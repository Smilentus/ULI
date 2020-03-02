import main
import alarm
import speaker
import time
from threading import Thread

alarmThread = Thread(target=alarm.initCounting, name='Alarm Thread', daemon=True)
mainThread = Thread(target=main.startCycle, name='Main Thread', daemon=True)
speakerThread = Thread(target=speaker.speakingCycle, name='Speaking Thread', daemon=True)

if __name__ == '__main__':
    alarmThread.start()
    mainThread.start()
    speakerThread.start()

    while(True):
        time.sleep(0.1)