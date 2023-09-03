import time
import board
import digitalio
from adafruit_motor import stepper

# Declaring global variables
global start, height, pos, t1, t1_prev, RTS_motor, VTS_motor
start = False
height = 5
pos = 1
start_time = 0
t1 = 0
t1_prev = 0

## MOTOR ##

def setup_motor(IN1, IN2):
    # set up motor command pins as outputs
    # Remember: these are the pins for the ARDUINO NANO RP2040 CONNECT not the Pico:

    dirPin = digitalio.DigitalInOut(IN1)
    dirPin.direction = digitalio.Direction.OUTPUT
    stepPin = digitalio.DigitalInOut(IN2)
    stepPin.direction = digitalio.Direction.OUTPUT

    # return the control pins
    return dirPin, stepPin

def rotate(end_pos, half=False): #finds most efficient path from current position
    global RTS_motor

    if not half:
        # calculate how many geneva rotations it would take to go from point A to B
        if pos < end_pos: # end_position value a larger number than start_position
            geneva_rot = (end_pos - pos) * 2 # x2 because 
            direction = stepper.FORWARD
            print("Moving Forward")
        elif pos > end_pos: # end_position value is a smaller number than start_position
            geneva_rot = (pos - end_pos) * 2
            direction = stepper.BACKWARD
            print("Moving Backward")
        else: #trying to prevent errors LOL
            geneva_rot = 0
            direction = stepper.FORWARD
    else: 
        # For the let go function
        geneva_rot = 1
        direction = stepper.FORWARD

    step_rot = 200 * geneva_rot

    # rotate geneva gear that many times
    for step in range(step_rot):
        RTS_motor.onestep(direction=direction)

    pos = end_pos

def vt(end_height): #changes height of arm #modify a lot
    global VTS_motor

    G_Geneva_gear_ratio = 200 # change this based on however Gerry designs the geneva gear

    # 1 = low
    # 5 = High (based on Eugene)

    if end_pos == 5:
        direction = stepper.FORWARD
    else:
        direction = stepper.BACKWARD

    for step in range(G_Geneva_gear_ratio):
        motor.onestep(direction=direction)

def pick_up(): #goes down, goes up
    # Assumes Starts up
    vt(1)
    vt(5)

def let_go(): #moves half, goes up
    global RTS_motor, VTS_motor
    # Assumes starts down
    rotate(RTS_motor, None, half=True) # disconnect magnet
    vt(VTS_motor, 5)
    rotate(RTS_motor, None, half=True) # reset back into the regular positions
    pos += 1 # (1/2 + 1/2) = 1

## PROCEDURE ##

def wait(duration):
    global t1, t1_prev
    while (t1 - t1_prev < duration):
        t1 = time.time() - start_time
        pass
    t1_prev += duration
    pass

# States
def load_meth(): # loading -> methanol
    print("Picking up the basket from the loading area.")
    rotate(1)
    pick_up()
    rotate(2)
    vt(1)
    print("STARTED: Methanol")

def meth_dry(): # methanol -> air dry
    print("FINISHED: Methanol")
    rotate(2)
    vt(5)
    rotate(3)
    vt(1)
    print("STARTED: Air Drying")

def dry_water1(): # air dry -> half water
    print("FINISHED: Air Drying")
    rotate(3)
    vt(5)
    rotate(4)
    vt(2)
    print("STARTED: Half Water")

def water1_stain(): # half water -> stain
    print("FINISHED: Half Water")
    rotate(4)
    vt(5)
    rotate(5)
    vt(1)
    let_go()
    rotate(1)
    print("STARTED: Staining")

def stain_water2(): # stain -> water
    print("FINISHED: Staining")
    rotate(5)
    pick_up()
    rotate(6)
    vt(1)
    let_go()
    print("STARTED: Full Water")

def water2_load(): # water -> loading
    print("FINISHED: Full Water")
    rotate(6)
    pick_up()
    rotate(1)
    let_go()
    print("The basket has been placed into the loading area.")

# Procedure Function
def procedure():
    global t1, t1_prev, start
    
    # 00:00 - 00:05: B1: loading -> methanol
    load_meth()
    wait(5)

    # 00:05 - 02:05: B1: methanol -> air dry
    meth_dry()
    wait(60 * 2)

    # 02:05 - 02:10: B1: air dry -> half water
    dry_water1()
    wait(5)

    # 02:10 - 22:10: B1: half water -> stain
    water1_stain()
    wait(20 * 60 - (2 * 60 + 10))

    # 20:00 - 20:05: B2: loading -> methanol
    load_meth()
    wait(5)

    # 20:05 - 22:05: B2: methanol -> air dry
    meth_dry()
    wait(60 * 2)

    # 22:05 - 22:10: B2: air dry -> half water
    dry_water1()
    wait(5)

    # 22:10 - 22:40: B1: stain -> water
    # 22:10 - 42:10: B2: half water -> stain
    stain_water2()
    water1_stain()
    wait(30)

    # 22:40 (DONE): B1: water -> loading
    water2_load()
    wait(20 * 60 - 30)

    # 42:10 - 42:40: B2: stain -> water
    stain_water2()
    wait(3)

    # 42:40 (DONE): B2: water -> loading
    water2_load()

    t1 = 0
    t1_prev = 0
    start = False

if __name__ == "__main__":
    if start:
        RTS_motor = setup_motor(board.GP17, board.GP16)
        VTS_motor = setup_motor(board.GP17, board.GP16) # change this to match circuit
        print(1)

    while 1:
        if start == True:
            start_time = time.time()
            procedure()