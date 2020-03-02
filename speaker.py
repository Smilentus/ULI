from logger import *
import pyttsx3
import pyaudio
import time

# Объект голосовой штучки
# Короче костыльное решение, потому что pyttsx3 с приколом
# Суть в том, что runAndWait() уходит в бесконечный цикл
class _TTS:
    engine = None

    def __init__(self):
        self.engine = pyttsx3.init()
    
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

queue = []

# Функции
def speak(what):
    queue.append(what)

def speakingCycle():
    while True:
        if len(queue) > 0:
            SystemLog('Started speak_engine ...')
            text = str(queue.pop(0))
            print(f'[SPEAKING] {text}')
            tts = _TTS()
            tts.speak(text)
            del(tts)
            SystemLog('Stopped speak_engine.')
        time.sleep(0.1)