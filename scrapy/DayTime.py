#encoding: utf-8
'''
初始化 年、月、日，天数增加，返回当前日期的字符串： 2014-01-01
'''

import datetime

class DateTime:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    def getCurStrOfCurDayTime(self):
        curDateTime = datetime.datetime(self.year, self.month, self.day)
        return str(curDateTime.strftime('%Y-%m-%d'))
    
    def increOneDay(self):
        curDateTime = datetime.datetime(self.year, self.month, self.day)
        delta = datetime.timedelta(days=1)
        nextDayTime = curDateTime + delta
        self.year = nextDayTime.year
        self.month = nextDayTime.month
        self.day = nextDayTime.day
    
    def getCurYear(self):
        return str(self.year)
    
    def getCurMonth(self):
        if (self.month <= 9):
            return '0' + str(self.month)
        return str(self.month)
    
    def getCurDay(self):
        if (self.day <= 9):
            return '0' + str(self.day)
        return str(self.day)
    
    def isLeapYear(self):
        year = int(self.year)
        if (0 == year % 4 and 0 != year % 100) or (0 == year % 400):
            return True
        return False