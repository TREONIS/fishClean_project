#!/usr/bin/python
# -*- coding: utf-8 -*-

# lib/dbHandler.py
# -----------------------
# This represents the database where the data will be logged.
# Its a collection of SQLite3 objects wrapped together for ease.


import sqlite3
import os
import sys

import utils

class sensorStoreBase():
    '''
    Base Sensor Database Object:
        This represents the database where the data will be logged. 
        Its a collection of SQLite3 objects wrapped together for ease.
        This base holds internal code for the class.
        
        if dbPath is left blank on initialisation it will use an in
        :memory: database
    '''
    connection = sqlite3.Connection
    cursor = sqlite3.Cursor
    dbPath = ''
    sensorTableName = ''
    
    def __init__(self, dbPath=':memory:', sensorTableName='sensorData'):
        self.dbPath = dbPath
        self.sensorTableName = sensorTableName
        self.connection = sqlite3.connect(self.dbPath)
        self.cursor = self.connection.cursor()
        self._checkDB()        
        
    def _checkDB(self):      
        sSQL = 'SELECT count(*) FROM sqlite_master WHERE type="table" AND name=?;'
        self.cursor.execute(sSQL, (self.sensorTableName,))
        ret = self.cursor.fetchone()
        if ret[0] == 0:
            self._createDB()        
            
    def _createDB(self):
        sSQL = 'CREATE TABLE ' + self.sensorTableName + '(id INTEGER PRIMARY KEY, date REAL, type TEXT, value REAL);'
        self.cursor.execute(sSQL)
            
    def test(self):
        sSQL = 'SELECT * from ' + self.sensorTableName + ';'
        self.cursor.execute(sSQL)
        ret = self.cursor.fetchall()
        for row in ret:
            print row             
        
class sensorStore(sensorStoreBase):
    '''
    Sensor Database Object:
        This represents the database where the data will be logged. 
        Its a collection of SQLite3 objects wrapped together for ease.
        
        if dbPath is left blank on initialisation it will use an in
        :memory: database
    '''
    
    def insertData(self, values):
        '''Inserts sensor values into database'''
        sSQL = 'INSERT INTO ' + self.sensorTableName + '(date, type, value) VALUES (:date, :type, :value);'
        insertDS = utils.prepareDataInsert(values)
        self.cursor.executemany(sSQL, insertDS)        
        #try:
            #self.cursor.execute(sSQL, dataSet)
        #except sqlite3.error, e:
            #print "Error %s:" % e.args[0]
            
            
if __name__ == '__main__':
    pass
    #test = sensorStore(':memory:')
    #valueList = {'ph':7.2,'light':512}
    #test.insertData(valueList)
    #test.test()