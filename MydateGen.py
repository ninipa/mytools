#!/usr/bin/python3
###############################################################################
# Author    :   Qianye Wu
# Email     :   ninipa1985@outlook.com
# Last modified : 2018-04-17 21:41
# Filename   : MydateGen.py
# Description    :  v0.2    --- change unit in list from int to str and zfill(2) to month/day
###############################################################################

# -*- coding: utf-8 -*-

import sys
import re
import calendar

class MydateGen(object):
    __doc__ = ''' Sending a startDate as "2018-04-17"(str) or "2018/04/17" And number of days count start from startDate as 365(int);
    return a list of date as [["2018","04","17"],["2018","04","18"]...]
    '''

    def __init__(self, startDate, dayNum):
        if not isinstance(startDate, str):
            sys.exit("[startDate] is not a string. Exit ...")
        elif not isinstance(dayNum, int):
            sys.exit("[dayNum] is not an int. Exit ...")
        else:
            pat = re.compile(r"(\d+)[\/-](\d+)[\/-](\d+)")
            date = pat.match((startDate))
            if date:
                self.startYear = int(date.group(1))
                self.startMonth = int(date.group(2))
                self.startDay = int(date.group(3))
                self.dayNum = dayNum
            else:
                sys.exit("[startDate] format is invalid. Exit")

    def gen_dates(self):
        #initialize vars
        year = self.startYear
        month = self.startMonth
        day = self.startDay
        dayNum = self.dayNum
        dateList = []
        #processing
        while dayNum >= (calendar.monthrange(year, month)[1]-day+1):
            daysThisMonth = calendar.monthrange(year, month)[1]-day+1
            #print("daysThisMonth = %s"%daysThisMonth)
            for i in range(0, daysThisMonth):
                dateList.append([year, month, day])
                day += 1
                if i == daysThisMonth-1:
                    day = 1
                    month += 1
                    if month == 13:
                        year += 1
                        month = 1
            dayNum -= daysThisMonth
            #print("dayNum = %s, year = %s, month = %s"%(dayNum, year, month))
        for i in range(0, dayNum):
            dateList.append([year, month, day])
            day += 1
        dateListStr = list(map(lambda dateUnit:[str(dateUnit[0]), str(dateUnit[1]).zfill(2), str(dateUnit[2]).zfill(2)], dateList))
        return dateListStr

if __name__ == "__main__":
    dateItem = MydateGen("2018-04-09", 100)
    dateList = dateItem.gen_dates()
    for date in dateList:
        print(date)


