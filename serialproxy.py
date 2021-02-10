import time
from threading import Thread

from serial import Serial

com1 = Serial('/dev/ttyUSB0', 115200, timeout=1)
com2 = Serial('/dev/ttyUSB1', 115200, timeout=1)


def pipe1():
    while True:
        b = com1.read(com1.in_waiting or 1)
        if b:
            com2.write(b)

def pipe2():
    while True:
        b = com2.read(com2.in_waiting or 1)
        if b:
            com1.write(b)

th1 = Thread(target=pipe1, daemon=True)
th2 = Thread(target=pipe2, daemon=True)
th1.start()
th2.start()

while True:
    time.sleep(1)
