import time
import datetime
import os
import random

from speaker import *
from logger import *

musicPath = "C:/Projects/Python/ULI-V4.0/alarms"
alarmTime = "9:47"
isActive = True

def initCounting():
    delta = 60 - datetime.datetime.now().second
    time.sleep(delta)

    while isActive:
        checkAlarm()
        time.sleep(60)

def checkAlarm():
    curTime = "{}:{}".format(datetime.datetime.now().hour, datetime.datetime.now().minute)

    if curTime == alarmTime:
        startAlarm()

def startAlarm():
    SystemLog('Будильник на {} сработал'.format(alarmTime))
    speak('Доброе утро, Дмитрий!')
    time.sleep(5)
    speak('Время просыпаться!')
    time.sleep(5)
    speak('Включаю крутую музыку для мотивации!')
    startMusic()

def startMusic():
    files = os.listdir(musicPath)

    print(len(files))
    sound = files[random.randint(0, len(files) - 1)]

    path = musicPath + "/" + sound
    print(path)

    os.startfile(path)

startMusic()
startMusic()
startMusic()
