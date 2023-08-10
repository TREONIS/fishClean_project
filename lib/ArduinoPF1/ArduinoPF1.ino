/*
    PF1 Serial interface
 --- ------ ---------
 
 This is a simple interface to talk to my python app on a
 python capable device via serial.
 
 It contains quite a few useful features that include:
 -* Reads data from sensors and sends it via
 serial with multiple formats when asked.
 -* Has an interface that allows the settings to be
 configured via serial.
 -* coded as pythonic and simple as i could with
 Arduino. The idea is for this to be simple
 and easily reusable for alternate projects.
 
 // Sensor Definitions 
 int iSensorCount = 1
 * Total Number of Sensors.
 * can be used to disable the higher numbered sensors.
 
 int sensor1Pin = 1
 char sensor1Type = 'd'
 * Example of typical Sensor Definition
 * 'd' = Digital
 * 'a' = Analog
 
 // General Settings
 char statusChar = '`'
 * Char to repeat over searial to signify waiting.
 
 int iExpire = 100
 * Total loops to complete before entering wait mode.
 
 int iMainDelay = 50
 * The number of miliseconds to pause in the mail loop.
 * This is linked to the iExpire variable in the sense
 that: 
 iExpire * iMainDelay = time in ms before going
 into wait mode.
 
 int iWaitDelay = 500
 * The number of miliseconds to wait between sending
 StatusChar when im wait mode.
 
 ~Patty
 11/12/2014
 
 Sleep Function taken from Sleep Demo Serial:
 Based on Sleep Demo Serial from http://www.arduino.cc/playground/Learning/ArduinoSleepCode 
 * Copyright (C) 2006 MacSimski 2006-12-30 
 * Copyright (C) 2007 D. Cuartielles 2007-07-08 - Mexico DF
 * With modifications from Ruben Laguna  2008-10-15
 * And more modifications from Patrick Coffey 2014-12-12
 
 *  This ,program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 * 
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 * 
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
 */

#include <avr/power.h>
#include <avr/sleep.h>
#include <stdlib.h>
#include "DHT.h"

// Sensor Definitions 
int iSensorCount = 3;

int sensorPins[] = {1, 1, 2}; 
char sensorTypes[] = {'d', 'a', 'D'};
String sensorNames[] = {"Leak", "Light", "DHT22"};
//---------------------

// General Settings
char statusChar = '`';
char cSeperator = ',';
int iExpire = 100;
int iMainDelay = 10;
int iWaitDelay = 500;
char cReadSensors = 'R';
char cSleep = 'P';
char cStatus = 'S';
//---------------------

// Other Settings/Globals
int inByte = 0;            //global
int iCountExp = 0;         //global
char serialIn[16];         //global
DHT dht(2, 'DHT22');
//---------------------

void setup() {
  Serial.begin(9600);
  initPins();
  sleepNow();
  //establishContact();                 // enter wait mode
}

void loop() {
  iCountExp += 1;
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) {
    // get incoming byte:
    inByte = Serial.read();
    if (inByte == 'R') {
      iCountExp = 0;
      // send sensor values
      String val = readSensors();
      Serial.print(val);   
    }
    if (inByte == 'P') {
      iCountExp = 0;
      sleepNow();                     // sleep function called here  
    }
    if (inByte == 'S') {
      iCountExp = 0;
      Serial.print(getStatus());
    }
  }
  if (iCountExp == iExpire) {
    iCountExp = 0;
    sleepNow();                       // Return to wait mode after timeout
  }
  delay(iMainDelay);
}

void sleepNow() {
  //Serial.println("Sleeping...");
  //delay(100);                         // this delay is needed, the sleep
  //function will provoke a Serial error otherwise!!
  set_sleep_mode(SLEEP_MODE_IDLE);

  sleep_enable();                     // enables the sleep bit in the mcucr register

  power_adc_disable();
  power_spi_disable();
  power_timer0_disable();
  power_timer1_disable();
  power_timer2_disable();
  power_twi_disable();

  sleep_mode();                       // here the device is actually put to sleep!!
  // <<THE PROGRAM CONTINUES FROM HERE AFTER WAKING UP
  sleep_disable();
  power_all_enable();
}

//void establishContact() {
//  while (Serial.available() <= 0) {
//    Serial.print(statusChar);         // send statusChar
//    delay(iWaitDelay);
//  }
//}

void initPins() {
  for (int i = 0; i < iSensorCount - 1; i++) {
    switch (sensorTypes[i]) {
    case 'd':
      //Digital Sensor
      pinMode(sensorPins[i], INPUT);
      break;
    case 'a':
      //Analog Sensor
      ;
      break;
    case 'D':
      //DHT22 Sensor
      ;
      break;
    }
  }
}

String getStatus() {
  String ret
  //add other logic here later if necesarry
  ret = "0 - Awake!";
  return ret;
}

String readDHT() {
  String ret;
  float h;
  float t;
  do {
    h = dht.readHumidity();
    t = dht.readTemperature();
    delay(50);
  } while (isnan(h) || isnan(t));
  char s[10];
  dtostrf(h, 1, 2, s);
  ret = "Humidity: ";
  ret += s;
  dtostrf(t, 1, 2, s);
  ret += ", Temp: ";
  ret += s;
  return ret;
}

String readSensors() {
  String ret;
  String val;
  for (int i = 0; i < (iSensorCount); i++) {
    if (i > 0) {
      ret += cSeperator;
    }
    ret += sensorNames[i];
    ret += ":";
    switch (sensorTypes[i]) {
    case 'd':
      //Digital Sensor
      int valD;
      valD = digitalRead(sensorPins[i]);
      val = String(valD, DEC);
      ret += val;
      break;
    case 'a':
      //Analog Sensor
      int valA;
      valA = analogRead(sensorPins[i]);
      val = String(valA, DEC);
      ret += val;
      break;
    case 'D':
      String valDHT;
      valDHT = readDHT();
      ret += valDHT;
      break;
    }
  }
  ret += "\n";
  return ret;
}  
