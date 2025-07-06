# -*- coding: utf-8 -*-

import os
import subprocess
import time

class Projector:

    def __init__(self, client, address=[]):
        self._client = client

        self._bootIndex = 0

        self._address = address
        self._boot = False
        self._moonlight = False

    def set_address(self, address):
        self._address = [int(i, 16) for i in address.split(':')]

    def subscribe(self):
        self._client.subscribe("ProjectorBoot006")
        self._client.subscribe("ProjectorMac")
        self._client.subscribe("ProjectorMoonlight006")

    def boot(self):
        print(f"Booting up projector...{self._address}")

        try:
            adv_data = "17 02 01 1A 03 03 12 18 0E FF 46 00 %02x %02x %02x %02x %02x %02x %02x FF FF FF FF" % (
                self._bootIndex,
                self._address[5], self._address[4], self._address[3],
                self._address[2], self._address[1], self._address[0])
            os.system(f"btmgmt -i hci0 advertising off")
            cmd = f"hcitool -i hci0  cmd 0x08 0x0008 {adv_data}"
            subprocess.run(cmd, shell=True, check=True)
            os.system("btmgmt -i hci0 advertising on")
            time.sleep(5)
        except:
            print("Error: Failed to send command to projector.")
        finally:
            os.system("btmgmt -i hci0 advertising off")

        self._bootIndex += 1
        if self._bootIndex > 255:
            self._bootIndex = 0

    def shutdown(self):
        print(f"Shutting down projector...{self._address}")

    def on_massage(self, topic, data):
        if topic == "ProjectorBoot006":
            if data == "on":
                self._boot = True
                self.boot()
            elif data == "off":
                self._boot = False
                self.shutdown()
            else:
                print("Unknown command.")
        elif topic == "ProjectorMac":
            self.set_address(data)
            print(f"Projector address set to {data}.")
        elif topic == "ProjectorMoonlight006":
            if data == "on":
                self._moonlight = True
                print("Moonlight mode enabled.")
            elif data == "off":
                self._moonlight = False
                print("Moonlight mode disabled.")
            else:
                print("Unknown command.")
        else:
            print(f"Unknown topic: {topic}.")