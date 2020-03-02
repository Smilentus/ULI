import os
import sys
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import datetime
import pyperclip
import saver
from threading import Thread

import alarm
from speaker import *
from logger import *
from dailyorganizer import *

# Глобальные переменные
RECOGNITION_LIMIT = 80

# Доступные команды
opts = {
    "alias": ('юля', 'юль', 'юленька', 'юляш', 'юла', 'юлик', 'юлия'),
    "tbr": ('что', 'покажи', 'на', 'скопировать', 'исключаемое', 'новое', 'пропускное', 'удаляемое', 'скопируй', 'дай', 'который', 'добавь', 'новая', 'запомни', 'выучи', 'сколько', 'по', 'сейчас', 'мне', 'какой', 'новую'),
    "cmds": {
        "ctime": ('время', 'час', 'часах'),
        "copy": ('смайлик', ),
        "learn_cmd": ('команду', 'команда'),
        "learn_alias": ('имя', 'алиас', 'кличка', 'кличку'),
        "learn_tbr": ('слово', 'исключение'),
        "open": ('открой', 'открыть', 'запусти', 'включи', 'запустить', 'включить'),
        "show_plans": ('уведомления', 'нотификации', 'планы', 'расписание'),
        "": (),
    }
}

# Программы для открытия
smthToOpen = {
    "notepad.exe": ('блокнот', 'черновик', 'записную книжку'),
    "calc.exe": ('калькулятор', ),
    "opera.exe": ('браузер', 'опера'),
    "regedit.exe": ('реестр', 'редактор реестра'),
    "control.exe": ('панель управления', ),
    "skype.exe": ('скайп', ),
    "discord.exe": ('дискорд', ),
    "cmd.exe": ('командную строку', 'power shell', 'кмд'),
}

# Что-то для копирования
smthToCopy = { 
    "¯\_(ツ)_/¯": ('разведение руками', 'не знаю', 'бывает', 'хм'),
    ":)": ('улыбка', 'радость', 'счастье'),
    ":D": ('смех') 
    }
    
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language='ru-RU').lower()
        SystemLog('Connected to Google Recognizer')
        Log('Распознано: ' + voice)
        SystemLog(f'Recognized something: {voice}')
        if voice.startswith(opts['alias']):
            cmd = voice

            SystemLog('Starting cleaning from alias ...')
            for x in opts['alias']:
                cmd = cmd.replace(x, '').strip()
            SystemLog('Cleaning ALIAS is done ...')
            SystemLog('CMD: ' + cmd)

            SystemLog('Starting cleaning from tbr ...')
            for x in opts['tbr']:
                cmd = cmd.replace(x, ' ').strip()
            SystemLog('Cleaning TBR is done ...')
            SystemLog('CMD: ' + cmd)

            SystemLog('Starting cleaning from double spaces ...')
            cmd = cmd.replace('  ', ' ').strip()
            SystemLog('CMD: ' + cmd)
            SystemLog('Cleaning DOUBLE SPACES is done ...')

            # Распознаю дополнительные аргументы из фразы
            SystemLog('Recognize EXTRA arguments ...')
            extra = ''
            for c, v in opts['cmds'].items():   
                for x in v:
                    if x in cmd:
                        extra = cmd.replace(x, '').strip()
            SystemLog('EXTRA: ' + extra)
            SystemLog('Recognizing EXTRA arguments is done ...')
            
            # Удаляем лишние аргументы из фразы
            SystemLog('Starting cleaning EXTRA arguments ...')
            cmd = cmd.replace(extra, '')
            SystemLog('Cleaning EXTRA arguments is done ...')

            cmd = recognize_cmd(cmd)
            if (cmd['percent'] >= RECOGNITION_LIMIT):
                execute_cmd(cmd['cmd'], extra)
            else:
                speak(f'Я распознала команду, но процент удовлетворения слишком маленький {cmd["percent"]}%!')
                SystemLog('Not enough cmd percentage ({} < {}%)'.format(cmd['percent'], RECOGNITION_LIMIT))
        else:
            Log('Текст не удовлетворяет запросу')

    except sr.UnknownValueError:
        Log('Голос не распознан!')
    except sr.RequestError as e:
        Log('Нет сигнала интернета. Проверьте интернет соединение! ... \n' + e)
    except Exception as e:
        Log('Незвестная природе ошибка: \n' + e)

def recognize_cmd(cmd):
    SystemLog('Starting CMD recognition ...')
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v: 
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    
    SystemLog('CMD recognition is done ...')
    SystemLog(f"CMD: {RC['cmd']} with {RC['percent']}%")
    return RC

def getSmileByCmd(extra):
    RC = {'smile': '', 'percent': 0}
    for c, v in smthToCopy.items():

        for x in v: 
            vrt = fuzz.ratio(extra, x)
            if vrt > RC['percent']:
                RC['smile'] = c
                RC['percent'] = vrt
    
    return RC
            
def getProgramByCmd(extra):
    RC = {'program': '', 'percent': 0}
    for c, v in smthToOpen.items():

        for x in v: 
            vrt = fuzz.ratio(extra, x)
            if vrt > RC['percent']:
                RC['program'] = c
                RC['percent'] = vrt
    
    return RC

def execute_cmd(cmd, extra=''):
    SystemLog('Starting CMD execution ...')
    SystemLog(f'Execute {cmd} CMD with {extra} arguments')
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak('Сейчас ' + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'copy':
        copyText = getSmileByCmd(extra)
        pyperclip.copy(copyText['smile'])
        speak(f'Скопировала {extra} в буфер обмена!')
        Log(f'Скопированный текст {copyText}')
    elif cmd == 'open':
        program = getProgramByCmd(extra)
        try:
            os.startfile(program['program'])
            speak('Запускаю программу')
        except FileNotFoundError as e:
            Log('Такой программы {} не существует!'.format(program['program']))
            speak('Не могу найти такую программу!')
    elif cmd == 'learn_cmd':
        pass
    elif cmd == 'learn_tbr':
        opts['tbr'] = opts['tbr'] + (extra, )
        speak(f'Добавила {extra} в список исключений')
        Log(f'Добавлено новое исключаемое слово: {extra}')
        saver.saveState(opts)
    elif cmd == 'learn_alias':
        opts['alias'] = opts['alias'] + (extra, )
        speak(f'Теперь меня можно называть {extra}')
        Log(f'Добавлен новый алиас: {extra}')
        saver.saveState(opts)
    elif cmd == 'show_plans':
        speak(checkNotifications())
    else:
        SystemLog(f'CMD: {cmd} is not recognized ...')
        Log(f'Команда не распознана: {cmd}')
        speak('Не могу распознать команду')
    SystemLog('CMD execution is done ...')
    
# Запуск
def startCycle():
    SystemLog('Loading commands ...')
    SystemLog('Initialising commands ...')

    SystemLog('Selecting microphone by device_index ...')
    r = sr.Recognizer()
    
    # SystemLog('Trying to find audio devices...')
    # for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #     print('{}) {}'.format(index, name))
    # SystemLog('Audio devices were found!')

    m = sr.Microphone(device_index=1)

    SystemLog('Adjusting for ambient noises ...')
    with m as source: 
        r.adjust_for_ambient_noise(source)

    # Информирование о том, что запланировано на сегодня
    SystemLog('Initialising notification system ...')
    initNotifications()
    SystemLog('Notification system loaded!')

    SystemLog('Initializing speak_engine ...')

    SystemLog('Saying hello to my greatest developer! (:*)')
 
    hour = datetime.datetime.now().hour
    if hour < 6:
        speak('Доброй ночи, Дмитрий!')
    elif hour < 12:
        speak('Доброе утро, Дмитрий!')
    elif hour < 18:
        speak('Добрый день, Дмитрий!')
    else:
        speak('Добрый вечер, Дмитрий!')     

    speak(checkNotifications())

    SystemLog('Start listening in background ...')
    stop_listening = r.listen_in_background(m, callback)