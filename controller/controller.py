from pyfirmata import Arduino, SERVO, boards
from pyfirmata.pyfirmata import Port
import time

port='COM4'

pin = 3
board = Arduino(port)
board.digital[pin].mode=SERVO

def rotateServo(pin, angle):
    board.digital[pin].write(angle)

def doorAutomate(val):
    if val==0:
        rotateServo(pin, 100)
        time.sleep(6)
        rotateServo(pin,0)
    elif val==1:
        rotateServo(pin, 0)