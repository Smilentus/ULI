import time
import datetime
import os
import random

from speaker import *
from logger import *

musicPath = "C:/Users/gilev/Music/alarms"
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
    curTime = "{}:{}".format(datetime.datetime.now().hour, datetime.datetime.now().minute)

    if curTime == alarmTime:
        startAlarm()
    SystemLog('Alarms checked succesfully!')

def startAlarm():
    SystemLog('Будильник на {} сработал'.format(alarmTime))
    speak('Доброе утро, Дмитрий!')
    speak('Время просыпаться!')
    speak('Включаю крутую музыку для мотивации!')
    startMusic()

def startMusic():
    files = os.listdir(musicPath)

    SystemLog("Кол-во доступных аудиозаписейи: " + len(files))
    sound = files[random.randint(0, len(files) - 1)]

    path = musicPath + "/" + sound
    SystemLog("Выбранная аудиодорожка: " + path)

    os.startfile(path)