"""
script to test different baud rates to test if they are accepted by the vending machine
"""

import serial

PORT = "/dev/ttyAMA0"
BAUDRATES= [1200, 2400, 4800, 9600]
TIMEOUT = 2

DOUBLE_ENQ = False
DELAY_TIME = 0.05

ENQ = b'\x05'
DLE = b'\x10'
ACK0 = b'\x30'
ACK1 = b'\x31'

if __name__ == '__main__':
    for baudrate in BAUDRATES:
        print("-------------------- Testing baudrate: ", baudrate)

        ser = serial.Serial(PORT, baudrate, timeout=TIMEOUT)
        ser.write(ENQ)
        if DOUBLE_ENQ:
            ser.write(ENQ)

        res = ser.read(2)
        if res:
            print("Machine answered to ENQ: ", res)
        else:
            print("Machine didnt answere to ENQ: ", res)

        if res:
            print("Answering machine...")
            ser.write(DLE+ACK1)

            res = ser.read(8912)
            if res:
                print("Machine answered to DLE: ", res)
            else:
                print("Machine didnt answere to DLE: ", res)


        ser.close()
