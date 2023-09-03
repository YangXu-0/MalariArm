# Write your code here :-)
import time
import board
import digitalio
#from adafruit_motor import stepper

# Declaring global variables
'''
global start, height, pos, t1, t1_prev, RTS_motor, VTS_motor, fin_prev_time
start = True
height = 5
pos = 1
start_time = 0
fin_prev_time = 0
t1 = 0
t1_prev = 0
'''

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

def rotate(RTS_motor, pos, end_pos, half=False): #finds most efficient path from current position
    #global RTS_motor, pos

    if not half:
        # calculate how many geneva rotations it would take to go from point A to B
        if pos < end_pos: # end_position value a larger number than start_position
            geneva_rot = (end_pos - pos) * 2 # x2 because
            CW = True
            print("Moving Forward")
        elif pos > end_pos: # end_position value is a smaller number than start_position
            geneva_rot = (pos - end_pos) * 2
            CW = False
            print("Moving Backward")
        else: #trying to prevent errors LOL
            geneva_rot = 0
            CW = True
        pos = end_pos
    else:
        # For the let go function
        geneva_rot = 1
        CW = True

    step_rot = 200 * geneva_rot

    RTS_motor[0].value = CW

    # rotate geneva gear that many times
    for step in range(step_rot):
        RTS_motor[1].value = True
        time.sleep(0.001)
        RTS_motor[1].value = False
        time.sleep(0.001)

    return pos

def vt(VTS_motor, height, end_height): #changes height of arm #modify a lot
    #global VTS_motor

    G_Geneva_gear_ratio = 200 # change this based on however Gerry designs the geneva gear

    # 1 = low
    # 5 = High (based on Eugene)

    if end_height == 5:
        direction = stepper.FORWARD
    else:
        direction = stepper.BACKWARD

    for step in range(G_Geneva_gear_ratio):
        motor.onestep(direction=direction)

    return end_height

def pick_up(VTS_motor): #goes down, goes up
    # Assumes Starts up
    height = 5
    height = vt(VTS_motor, height, 1)
    height = vt(VTS_motor, height, 5)

def let_go(): #moves half, goes up
    #global RTS_motor, VTS_motor, pos

    # Assumes starts down
    pos = rotate(1, half=True) # disconnect magnet
    height = vt(VTS_motor, 1, 5)
    pos = rotate(1, half=True) # reset back into the regular positions
    pos += 1 # (1/2 + 1/2) = 1

## PROCEDURE ##

def wait(t1, t1_prev, fin_prev_time, duration):
    global start_cur_time

    duration += time.time() - fin_prev_time

    start_cur_time = time.time() #

    while (t1 - t1_prev < duration):
        t1 = time.time() - start_time
        pass
    t1_prev += duration

    print(time.time() - start_cur_time) #
    fin_prev_time = time.time()

    return t1, t1_prev, fin_prev_time

# States
def load_meth(RTS_motor, VTS_motor, pos, height): # loading -> methanol
    print("Picking up the basket from the loading area.")
    pos = rotate(RTS_motor, pos, 1)
    pick_up(VTS_motor)
    pos = rotate(RTS_motor, pos, 2)
    height = vt(VTS_motor, height, 1)
    print("STARTED: Methanol")

    return pos, height

def meth_dry(RTS_motor, VTS_motor, pos, height): # methanol -> air dry
    print("FINISHED: Methanol")
    pos = rotate(RTS_motor, pos, 2)
    height = vt(VTS_motor, height, 5)
    pos = rotate(RTS_motor, pos, 3)
    height = vt(VTS_motor, height, 1)
    print("STARTED: Air Drying")

    return pos, height

def dry_water1(RTS_motor, VTS_motor, pos, height): # air dry -> half water
    print("FINISHED: Air Drying")
    pos = rotate(RTS_motor, pos, 3)
    height = vt(VTS_motor, height, 5)
    pos = rotate(RTS_motor, pos, 4)
    height = vt(VTS_motor, height, 2)
    print("STARTED: Half Water")

    return pos, height

def water1_stain(RTS_motor, VTS_motor, pos, height): # half water -> stain
    print("FINISHED: Half Water")
    pos = rotate(RTS_motor, pos, 4)
    height = vt(VTS_motor, height, 5)
    pos = rotate(RTS_motor, pos, 5)
    height = vt(VTS_motor, height, 1)
    let_go()
    pos = rotate(RTS_motor, pos, 1)
    print("STARTED: Staining")

    return pos, height

def stain_water2(RTS_motor, VTS_motor, pos, height): # stain -> water
    print("FINISHED: Staining")
    pos = rotate(RTS_motor, pos, 5)
    pick_up()
    pos = rotate(RTS_motor, pos, 6)
    height = vt(VTS_motor, height, 1)
    let_go()
    print("STARTED: Full Water")

    return pos, height

def water2_load(RTS_motor, VTS_motor, pos, height): # water -> loading
    print("FINISHED: Full Water")
    pos = rotate(RTS_motor, pos, 6)
    pick_up()
    pos = rotate(RTS_motor, pos, 1)
    let_go()
    print("The basket has been placed into the loading area.")

    return pos, height

# Procedure Function
def procedure(RTS_motor, VTS_motor, pos, height, start_time):
    t1 = 0
    t1_prev = 0
    fin_prev_time = 0

    # 00:00 - 00:05: B1: loading -> methanol
    pos, height = load_meth(RTS_motor, VTS_motor, pos, height)
    fin_prev_time = time.time()
    t1, t1_prev, fin_prev_time = wait(t1, t1_prev, fin_prev_time, 5)

    # 00:05 - 02:05: B1: methanol -> air dry
    pos, height = meth_dry(RTS_motor, VTS_motor, pos, height)
    #wait(60 * 2)
    t1, t1_prev, fin_prev_time = wait(t1, t1_prev, fin_prev_time, 5)

    # 02:05 - 02:10: B1: air dry -> half water
    pos, height = dry_water1(RTS_motor, VTS_motor, pos, height)
    t1, t1_prev, fin_prev_time = wait(t1, t1_prev, fin_prev_time, 5)

    # 02:10 - 22:10: B1: half water -> stain
    pos, height = water1_stain(RTS_motor, VTS_motor, pos, height)
    #wait(20 * 60 - (2 * 60 + 10))
    t1, t1_prev, fin_prev_time = wait(t1, t1_prev, fin_prev_time, 5)

    # 20:00 - 20:05: B2: loading -> methanol
    pos, height = load_meth(RTS_motor, VTS_motor, pos, height)
    t1, t1_prev, fin_prev_time = wait(t1, t1_prev, fin_prev_time, 5)

    # 20:05 - 22:05: B2: methanol -> air dry
    pos, height = meth_dry(RTS_motor, VTS_motor, pos, height)
    #wait(60 * 2)
    t1, t1_prev, fin_prev_time = wait(t1, t1_prev, fin_prev_time, 5)

    # 22:05 - 22:10: B2: air dry -> half water
    pos, height = dry_water1(RTS_motor, VTS_motor, pos, height)
    t1, t1_prev, fin_prev_time = wait(t1, t1_prev, fin_prev_time, 5)

    # 22:10 - 22:40: B1: stain -> water
    # 22:10 - 42:10: B2: half water -> stain
    pos, height = stain_water2(RTS_motor, VTS_motor, pos, height)
    pos, height = water1_stain(RTS_motor, VTS_motor, pos, height)
    #wait(30)
    t1, t1_prev, fin_prev_time = wait(t1, t1_prev, fin_prev_time, 10)

    # 22:40 (DONE): B1: water -> loading
    pos, height = water2_load(RTS_motor, VTS_motor, pos, height)
    #wait(20 * 60 - 30)
    t1, t1_prev, fin_prev_time = wait(t1, t1_prev, fin_prev_time, 10)

    # 42:10 - 42:40: B2: stain -> water
    pos, height = stain_water2(RTS_motor, VTS_motor, pos, height)
    #wait(30)
    t1, t1_prev, fin_prev_time = wait(t1, t1_prev, fin_prev_time, 10)

    # 42:40 (DONE): B2: water -> loading
    pos, height = water2_load(RTS_motor, VTS_motor, pos, height)

    t1 = 0
    t1_prev = 0
    start = False

def testing(RTS_motor, VTS_motor, test_rts=False, test_vts=False):
    if test_rts == True:
        RTS_motor[0].value = True
        for i in range(200):
            RTS_motor[1].value = True
            time.sleep(0.009)
            RTS_motor[1].value = False
            time.sleep(0.009)
        RTS_motor[0].value = True
        for i in range(200):
            RTS_motor[1].value = True
            time.sleep(0.009)
            RTS_motor[1].value = False
            time.sleep(0.009)
            
    if test_vts == True:
        VTS_motor[0].value = True
        for i in range(200):
            VTS_motor[1].value = True
            time.sleep(0.009)
            VTS_motor[1].value = False
            time.sleep(0.009)
        VTS_motor[0].value = False
        for i in range(200):
            VTS_motor[1].value = True
            time.sleep(0.009)
            VTS_motor[1].value = False
            time.sleep(0.009)                           

if __name__ == "__main__":
    start = True
    pos = 1
    height = 5
    RTS_motor = setup_motor(board.GP17, board.GP16)
    VTS_motor = setup_motor(board.GP17, board.GP16) # change this to match circuit

    while 1:
        if start:
            start_time = time.time()
            #procedure(start_time, pos, height, RTS_motor, VTS_motor, start_time)
            testing(RTS_motor, VTS_motor, test_vts=True)
            print("DONE!"),