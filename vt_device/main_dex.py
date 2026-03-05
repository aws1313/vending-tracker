import serial
import datetime
import os

PORT = "/dev/ttyS0"
BAUD = 9600
TIMEOUT = 2

class DEXReader:
    def __init__(self):
        self.ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)

    def get_data(self):
        self.ser.write(b"\x05")

        raw_data = self.ser.read(8192)

        if raw_data:
            print("Daten erfolgreich geladen")

        else:
            print("Keine Antwort vom Automaten erhalten.")

        #

        return raw_data

    def receive_save(self):
        raw = self.get_data()
        with open(f"raw_data_{datetime.datetime.now().isoformat()}", "wb") as f:
            f.write(raw)

        print("---- Daten: ----")
        print(raw.decode("ascii", errors="ignore"))

    def close(self):
        self.ser.close()


if __name__ == '__main__':
    dex = DEXReader()
    dex.receive_save()
    dex.close()