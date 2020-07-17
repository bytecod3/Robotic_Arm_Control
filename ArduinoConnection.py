from pyfirmata import Arduino, util
from time import sleep
import serial


def create_arduino_connection(port='COM13'):
    try:
        port = port
        board = Arduino(port)
        sleep(3)
        it = util.Iterator()
        it.start()
        return True
    except serial.serialutil.SerialException:
        return False

