import json
import requests
from threading import Thread, Lock, Event
from queue import Queue, Empty

import board
import adafruit_tca9548a
from adafruit_ina219 import INA219

class BackgroundCheck(Thread):
    def __init__(self, queue, rows, columns):
        Thread.__init__(self)
        self.daemon = True
        self.queue = queue
        self.rows = rows
        self.columns = columns

    def run(self):
        pass



class VTDevice:
    def __init__(self, conf:str = "config.json"):
        with open(conf) as f:
            self.conf = json.load(f)

        self.server = self.conf["server"]
        self.apikey = self.conf["apikey"]

        self.i2c = board.I2C()
        self.tca = adafruit_tca9548a.TCA9548A(self.i2c)
        self.available_addresses = self.tca_scan()
        self.rows, self.columns = self.init_sensors()

        self.sold_queue = Queue()

        self.background_check = BackgroundCheck()


    def init_sensors(self):
        r: list[INA219] = []
        c: list[INA219] = []

        i:str
        for i in self.conf["rows"]:
            ch, a = i.split(":")
            r.append(INA219(i2c_bus=self.tca[int(ch)], addr=int(f"0x{a}",16)))

        for i in self.conf["columns"]:
            ch, a = i.split(":")
            c.append(INA219(i2c_bus=self.tca[int(ch)], addr=int(f"0x{a}",16)))

        return r, c

    def tca_scan(self):
        a = []
        for c in range(8):
            if self.tca[c].try_lock():
                ad = self.tca[c].scan()
                for d in ad:
                    a.append(f"{c}:{d}")

                self.tca[c].unlock()
        return a

    def item_sold(self, r, c):
        resp = requests.patch(f"{self.server}/api/itemsold/{r}/{c}")


    def run(self):
        self.background_check.start()

        while True:
            try:
                item = self.sold_queue.get(timeout=0.1)
            except Empty:
                continue
            else:
                r, c = item
                self.item_sold(r,c)
                self.sold_queue.task_done()

if __name__ == '__main__':
    VTDevice().run()