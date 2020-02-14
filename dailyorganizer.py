import datetime
import os
from logger import *
from extraclasses import SheetBlock

# TODO: Внедрить умное расписание по дням и т.п.
# Формат: yyyy-mm-dd hh-mm-ss
# Расписание на день
daily_sheet = []

# Все когда-либо запланированные мероприятия
planning_sheet = []
    
def isDateExists(date):
    for d in planning_sheet:
        if d.date == date:
            return True, 
    return False

def getIndexOf(date):
    for i in range(len(planning_sheet)):
        if planning_sheet[i].date == date:
            return i
    return None

def addNotification(date, time, text):
    SystemLog('Add notification w/ {} on {} to {}'.format(text, time, date))
    if isDateExists(date):
        index = getIndexOf(date)
        if index is None:
            SystemLog('Can not find notification to {}'.format(date))
            return
        planning_sheet[index].addNotifications(time, text)
    else:
        line = SheetBlock(date)
        line.addNotifications(time, text)
        planning_sheet.append(line)
    SystemLog('Notifications added succesfully!')

def delNotification():
    pass

def initNotifications():
    SystemLog('Initialize notifications ...')
    now = datetime.datetime.now()
    for c in planning_sheet:
        if now.date() == datetime.datetime.strptime(c.date, "%Y-%m-%d").date():
            daily_sheet.append(c)
    SystemLog('Notifications initialized succesfully!')

def checkNotifications():
    SystemLog('Check notifications for today ...')
    data = 'Планы на сегодня: '
    for m in daily_sheet:
        data += m.getNotifications()
    
    if len(daily_sheet) == 0:
        data = 'На сегодня нет запланированных дел!'

    return data