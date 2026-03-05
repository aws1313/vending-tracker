"""
script to test if the RS232 controller is working at all.
for testing: short tx and rx of the RS232 controller and run the script
"""

import serial

PORT = "/dev/ttyAMA0"
BAUD = 9600
TIMEOUT = 2

if __name__ == '__main__':
    ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
    ser.write(b'Hello World! This is a test.')

    res = ser.read(8192)
    print(res)

    ser.close()

