#!/usr/bin/python
# -*- coding: utf-8 -*-

# lib/arduinoCom.py
# -----------------
# This is the class for the arduiono communication object.
# Its basically just a wrapper for a the serial object
# but it has a bit of extra arduino specific finctionality.


from serial import Serial
import time

class serialComBase(Serial):
    """
    Base Serial Communication Object:
        This represents a device connected via serial to the host. 
        This class houses all the code used internally to the function.
        Other classes can inherit from this and add user functions.
        
        communicates using packets, an example:
            
        
        Check pySerial Documentation
    """
    
    # using PPP special chars
    HEADER_CHAR = 0x7E
    FOOTER_CHAR = 0x7E
    ESCAPE_CHAR = 0x7D
    
    STATUS_AWAKE = '0 - Awake!'
    STATUS_BUSY = '1 - Busy!'
    CHAR_READ = 'R'
    CHAR_STATUS = 'S'
    CHAR_SLEEP = 'P'
    
    def __init__(self, comPort='/dev/ttyACM0', baudRate=9600):
        """Overloaded to set default values - Check pySerial Documentation"""
        Serial.__init__(self, comPort, baudRate)
        print("Initialised Serial connection")
        time.sleep(3)

    def _readChar(self):
        """Read a single byte from the Serial buffer"""
        ret = ''
        if self.isOpen():
            ret = self.read(1)
            return(ret)
        
    def _readBuff(self):
        """Read the Serial buffer and return each char one at a time like a generator"""
        ret = ''
        if self.isOpen():
            while self.inWaiting > 0:
                ret = self.read(1)
                yield ret    
                
    def _hasChars(self):
        """Checks if there are characters in the serial buffer"""
        ret = ''
        if self.isOpen():
            while self.inWaiting > 0:
                return True
            else:
                return False
        else:
            return 2
    
    def _wrapPacket(self):
        """Wraps the data/command into a packet to transmit"""
        pass
    
    def _unwrapPacket(self):
        """Unwraps the data/commands in the recieved packet"""
        pass
    
    def _getStream(self):
        """Gets the Stream of data form the device using self._readBuff"""
        inMessage = False
        inEscape = False
        ret = ''
        while self._hasChars():
            for char in self._readBuff():
                if inEscape == False:
                    if char == self.HEADER_CHAR:
                        if inMessage == False:
                            inMessage = True 
                    elif char == self.ESCAPE_CHAR:
                        inEscape = True
                    else:
                        ret += char
                elif inEscape == True:
                    if inMessage == True:
                        ret += char
        if ret == '':
            return 2
        else:
            return ret
    
    def _processData(self, data):
        ret = {}
        sensors = str.split(data, ',')
        for sensor in sensors:
            temp = str.split(sensor, ':')
            ret[str.strip(temp[0])] = float(str.strip(temp[1]))
        return ret
        

class ArduinoCom(serialComBase):
    """
    Arduino Communication Object:
        This represents the arduino connected via serial. 
        It is basically the Serial class from pySerial wrapped into
        a class with a few extra arduino specific functions.
        
        Check pySerial Documentation
    """
    
    def arduinoIsReady(self):
        """Gets the status of the Arduino, can be used to check if it is ready"""
        ret = ''
        if self.isOpen():
            self.flush()
            self.write(self.CHAR_STATUS)
            time.sleep(0.5)
            ret = self.readline()
            if ret == self.STATUS_AWAKE:
                return True
            else:
                return False
            
    def arduinoGetSensors(self):
        """Gets the sensor values from the Arduino"""
        ret = {}
        if self.arduinoIsReady():
            self.flush()
            self.write(self.CHAR_READ)
            time.sleep(0.5)
            ret = self._processData(self.readline())
            return(ret)

    def arduinoSleep(self):
        """Puts the Arduino to sleep by calling the sleep function in PF1 Firmware"""
        ret = ''
        if self.arduinoIsReady():
            self.flush()
            self.write(self.CHAR_SLEEP)
            time.sleep(0.5)


if __name__ == "__main__":
    pass
    #derp = _processData('light: 512, ph: 7.2')
    #print derp
    
    arduino = ArduinoCom()
    while arduino.isOpen():
        print(arduino.arduinoGetSensors())