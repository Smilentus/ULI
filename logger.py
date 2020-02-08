SHOW_SYSTEM_LOG = True
SHOW_LOG = True

def Log(text):
    if SHOW_LOG is True:
        print(f'[LOG] {text}')

def SystemLog(text):
    if SHOW_SYSTEM_LOG is True:
        print(f'[SYSTEM] {text}')

def CustomLog(caption, text):
    print(f'[{caption}] {text}')