import time
import board
import digitalio
from adafruit_motor import stepper
from timer import Timer

# Declaring global variables
## Note from Joaquin: Double check how to declare global variables. I'm getting syntax errors
start = False
height = 5
pos = 1 # tracks the current position of the arm for path finding
t1 = Timer()
t1_prev = 0

### Joaquin part: Integration

## Important notes:
# each function will require the passing in of whatever motor you are using
# Stepper motors have 200 distinct movement locations (google) so to complete 1 geneva rotation
# you need 200 steps
# Please change the pins at the bottom in the main function for testing.
# VTS function will probably need work

# Later note: I figured out why the global variable stuff isn't working and I fixed it.

def setup_motor(IN1, IN2, IN3, IN4):
    # set up motor command pins as outputs
    # Remember: these are the pins for the ARDUINO NANO RP2040 CONNECT not the Pico:
    coils = (digitalio.DigitalInOut(IN1),  #IN4
        digitalio.DigitalInOut(IN2),       #IN3
        digitalio.DigitalInOut(IN3),       #IN2
        digitalio.DigitalInOut(IN4))       #IN1
    for coil in coils:
        coil.direction = digitalio.Direction.OUTPUT

    # use the stepper motor library to set up motor output
    motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)

    return motor

def pick_up(motor): #goes down, goes up
    # Assumes Starts up
    vts(motor, 1)
    vts(motor, 5)

def let_go(): #moves half, goes up
    # Assumes starts down
    rotate(motor, None, half=True) # disconnect magnet
    vts(motor, 5)
    rotate(motor, None, half=True) # reset back into the regular positions
    pos += 1 # (1/2 + 1/2) = 1

def rotate(motor, end_pos, half=False): #finds most efficient path from current position
    if half == False:
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
        motor.onestep(direction=direction)

    pos = end_pos

def vt(motor, end_height): #changes height of arm #modify a lot
    G_Geneva_gear_ratio = 200 # change this based on however Gerry designs the geneva gear

    # 1 = low
    # 5 = High (based on Eugene)

    if end_pos == 5:
        direction = stepper.FORWARD
    else:
        direction = stepper.BACKWARD

    for step in range(G_Geneva_gear_ratio):
        motor.onestep(direction=direction)


# States
def procedure(RTS_motor, VTS_motor):
    t1.start()

    # 00:00 - 00:05: B1: loading -> methanol
    load_meth(RTS_motor, VTS_motor)
    wait(5)

    # 00:05 - 02:05: B1: methanol -> air dry
    meth_dry(RTS_motor, VTS_motor)
    wait(60 * 2)

    # 02:05 - 02:10: B1: air dry -> half water
    dry_water1(RTS_motor, VTS_motor)
    wait(5)

    # 02:10 - 22:10: B1: half water -> stain
    water1_stain(RTS_motor, VTS_motor)
    wait(20 * 60 - (2 * 60 + 10))

    # 20:00 - 20:05: B2: loading -> methanol
    load_meth(RTS_motor, VTS_motor)
    wait(5)

    # 20:05 - 22:05: B2: methanol -> air dry
    meth_dry(RTS_motor, VTS_motor)
    wait(60 * 2)

    # 22:05 - 22:10: B2: air dry -> half water
    dry_water1(RTS_motor, VTS_motor)
    wait(5)

    # 22:10 - 22:40: B1: stain -> water
    # 22:10 - 42:10: B2: half water -> stain
    stain_water2(RTS_motor, VTS_motor)
    water1_stain(RTS_motor, VTS_motor)
    wait(30)

    # 22:40 (DONE): B1: water -> loading
    water2_load(RTS_motor, VTS_motor)
    wait(20 * 60 - 30)

    # 42:10 - 42:40: B2: stain -> water
    stain_water2(RTS_motor, VTS_motor)
    wait(3)

    # 42:40 (DONE): B2: water -> loading
    water2_load(RTS_motor, VTS_motor)

    t1.stop()
    pass

def wait(duration):
    while (t1 - t1_prev < duration):
        pass
    t1_prev += duration
    pass

def load_meth(RTS_motor, VTS_motor): # loading -> methanol
    rotate(RTS_motor, 1)
    pick_up()
    rotate(RTS_motor, 2)
    vt(1)
    pass

def meth_dry(RTS_motor, VTS_motor): # methanol -> air dry
    rotate(RTS_motor, 2)
    vt(5)
    rotate(RTS_motor, 3)
    vt(1)

def dry_water1(RTS_motor, VTS_motor): # air dry -> half water
    rotate(RTS_motor, 3)
    vt(5)
    rotate(RTS_motor, 4)
    vt(2)

def water1_stain(RTS_motor, VTS_motor): # half water -> stain
    rotate(RTS_motor, 4)
    vt(5)
    rotate(RTS_motor, 5)
    vt(1)
    let_go()
    rotate(RTS_motor, 1)

def stain_water2(RTS_motor, VTS_motor): # stain -> water
    rotate(RTS_motor, 5)
    pick_up()
    rotate(RTS_motor, 6)
    vt(1)
    let_go()

def water2_load(RTS_motor, VTS_motor): # water -> loading
    rotate(RTS_motor, 6)
    pick_up()
    rotate(RTS_motor, 1)
    let_go()

if __name__ == "__main__":
    if start:
        RTS_motor = setup_motor(board.D2, board.D3, board.D4, board.D5) # change this to match circuit
        VTS_motor = setup_motor(board.D2, board.D3, board.D4, board.D5) # change this to match circuit
        print(1)

    while 1:
        if start == True:
            procedure(RTS_motor, VTS_motor)