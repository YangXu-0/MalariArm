from timer import Timer

# Declaring global variables
start = False
height = 5
pos = 1
t1 = Timer()
t1_prev = 0

# States
def procedure():
    global t1

    t1.start()

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

    t1.stop()
    pass

def wait(duration):
    global t1, t1_prev
    while (t1 - t1_prev < duration):
        pass
    t1_prev += duration
    pass

def load_meth(): # loading -> methanol
    rotate(1)
    pick_up()
    rotate(2)
    vt(1)
    pass

def meth_dry(): # methanol -> air dry
    rotate(2)
    vt(5)
    rotate(3)
    vt(1)

def dry_water1(): # air dry -> half water
    rotate(3)
    vt(5)
    rotate(4)
    vt(2)

def water1_stain(): # half water -> stain
    rotate(4)
    vt(5)
    rotate(5)
    vt(1)
    let_go()
    rotate(1)

def stain_water2(): # stain -> water
    rotate(5)
    pick_up()
    rotate(6)
    vt(1)
    let_go()

def water2_load(): # water -> loading
    rotate(6)
    pick_up()
    rotate(1)
    let_go()

if __name__ == "__main__":
    global start

    if start:
        print(1)

    while 1:
        if start == True:
            procedure()