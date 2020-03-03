import time
import datetime
import os
import random

from speaker import *
from logger import *

musicPath = "C:/Users/gilev/Music/alarms/"
alarmTime = "8:00"
isActive = True

def initCounting():
    SystemLog('Start calibration of alarm time counter ...')
    delta = 60 - datetime.datetime.now().second
    time.sleep(delta)
    SystemLog('Alarm time counter calibrated!')

    while True:
        checkAlarm()
        time.sleep(60)

def checkAlarm():
    SystemLog('Checking alarms ...')
    hours = datetime.datetime.now().hour
    minutes = datetime.datetime.now().minute
    
    if minutes < 10:
        minutes = '0{}'.format(minutes)

    curTime = "{}:{}".format(hours, minutes)

    print(curTime)

    if curTime == alarmTime:
        startAlarm()
    SystemLog('Alarms checked succesfully!')

def startAlarm():
    SystemLog('Будильник на {} сработал'.format(alarmTime))
    speak('Доброе утро, Дмитрий!')
    time.sleep(3)
    speak('Пора просыпаться!')
    time.sleep(3)
    speak('Время ' + alarmTime + ". Сегодня " + getWeekDay())
    time.sleep(3)
    # speak('Погода на сегодня: ')
    # time.sleep(3)
    speak('Включаю крутую музыку для мотивации!')
    time.sleep(3)
    startMusic()

def getWeekDay():
    sheet = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    return sheet[datetime.datetime.weekday(datetime.datetime.now())]

def getWeatherInfo():
    return 'Nothing'

def startMusic():
    files = os.listdir(musicPath)

    sound = files[random.randint(0, len(files) - 1)]

    path = musicPath + "/" + sound

    os.startfile(path)