#!/usr/bin/python
# -*- coding: utf-8 -*-

# fishtankMon - lib/utils.py
# -----------------------
# Misc. utilities

import os

def flashArduino():
    '''Flash PF1 firmware to arduino'''
    resetArduino()
    pass

def resetArduino():
    '''Reset the arduino. Useful for flashing or when it has hung.'''
    pass

#def updatePF1():
    #'''Sets current settings from lib/arduinoCom.py to ArduinoPF1.ino'''
    #variables = ['iSensorCount',
                 #'sensorPins', 
                 #'sensorTypes', 
                 #'sensorNames', 
                 #'cSeperator', 
                 #'iExpire', 
                 #'iMainDelay', 
                 #'iWaitDelay', 
                 #'cReadSensors',
                 #'cSleep',
                 #'cStatus']
    
    #cwd = os.getcwd()
    #strPF1 = cwd + '/arduinoPF1/arduinoPF1.ino'
    #strArduinoCom = cwd + '/arduinoCom.py'
    ##get the settings from the ArduinoCom.py file
    #with open(strPF1) as PF1:
        #strFileData = PF1.read()
        #for line in strFileData():
            #if line






if __name__ == '__main__':
    pass
