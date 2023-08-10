#!/usr/bin/python
# -*- coding: utf-8 -*-

# fishtankMon - main.py
# -----------------------
# This is the main program logic

import lib.arduinoCom as arduinoCom
import lib.dbHandler as dbHandler
import lib.utils as utils

import time


if __name__ == '__main__':
    arduino = arduinoCom.ArduinoCom()
    db = dbHandler.sensorStore()

    counter = 0

    while arduino.isOpen():
        counter += 1
        data = arduino.arduinoGetSensors()
        db.insertData(data)
    
        if counter == 10:
            counter = 0
            db.test()
    
        time.sleep(1)