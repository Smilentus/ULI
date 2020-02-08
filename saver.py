import os
from logger import *

DEFAULT_PATH = './opts/'

def writeToFile(path, values):
    try:
        with open(DEFAULT_PATH + path, 'w', encoding='utf-8') as file_handler:
            for line in values[:-1]:
                file_handler.write('{};'.format(line))
            file_handler.write(values[-1])
    except IOError as e:
        CustomLog('[SAVER] ', "An IOError has occurred!")
        CustomLog('[ERROR] ', e)

def readFromFile(path):
    try:
        lines = []
        with open(DEFAULT_PATH + path, 'r', encoding='utf-8') as file_handler:
            lines = file_handler.read().split(';')
        return lines
    except IOError as e:
        CustomLog('[SAVER] ', "An IOError has occurred!")
        CustomLog('[ERROR] ', e)

def saveState(opts):
    
    writeToFile('alias.txt', opts['alias'])
    writeToFile('tbr.txt', opts['tbr'])
    
    for n, o in opts['cmds'].items():
        writeToFile('cmds/{}.txt'.format(n), o)

def loadState():
    opts = {}

    alias = readFromFile('alias.txt')
    opts.update({'alias': tuple(alias)})
    tbr = readFromFile('tbr.txt')
    opts.update({'tbr': tuple(tbr)})

    files = os.listdir(DEFAULT_PATH + 'cmds/')
    opts.update({'cmds': {}})
    for f in files:
        data = readFromFile('cmds/' + f)
        opts['cmds'].update({f.replace('.txt', ''): tuple(data)})
    
    return opts