from logger import *
import pyttsx3
import pyaudio

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

# Функции
def speak(what):
    SystemLog('Started speak_engine ...')
    print(f'[SPEAKING] {what}')
    tts = _TTS()
    tts.speak(str(what))
    del(tts)
    SystemLog('Stopped speak_engine.')