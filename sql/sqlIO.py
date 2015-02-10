#!/usr/bin/env python
# encoding: utf-8

"""
IO for sqlite3
"""
# Copyright (C) by 
# Chu Yanshuo <chu@yanshuo.name>
# All rights reserved

import sqlite3

class SQLIO():

    """IO"""

    #operators
    #insert a row of data

    def __init__(self, dbFile):

        self.conn = sqlite3.connect(dbFile)

    def push(self, **entry):
        """push an entry to db

        :*entry: @todo
        :returns: @todo

        """
        insertOpStr = "INSERT INTO {0} VALUES ('{1}',{2},'{3}','{4}','{5}','{6}')"
        print (insertOpStr.format('lotteryData' ,entry['time'], entry['number'], entry['lotteryNumber'], entry['decade'], entry['unit'], entry['lastThree']))
        print self.conn.execute(insertOpStr.format('lotteryData' ,entry['time'], entry['number'], entry['lotteryNumber'], entry['decade'], entry['unit'], entry['lastThree']))
        self.conn.commit()

    def removeLastEntry(self):
        """remove last entry of current table
        :returns: @todo

        """
    
    def isFull(self, length):
        """if the table size equals length

        :length: @todo
        :returns: @todo

        """

    def hasThis(self, **entry):
        """@todo: prevent the duplicate items

        :**entry: @todo
        :returns: @todo

        """
        pass
        

if __name__ == '__main__':
    sqlio = SQLIO("lottery.db")
    sqlio.push(time = '2015-01-1', number = 8, lotteryNumber = '12343', decade = '大双', unit = '小单', lastThree = '大双')
    sqlio.conn.close()

