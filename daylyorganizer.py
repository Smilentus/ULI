import datetime
import os

# TODO: Внедрить умное расписание по дням и т.п.
# Формат: yyyy-mm-dd hh-mm-ss
daily_sheet = []

# Все когда-либо запланированные действия
planning_sheet = {
    "2020-02-14": ('Первое дело', 'Второе дело', 'Третье дело'),
    "2020-02-15": ('Дело номер 1', 'Дело номер 2'),
    "2020-02-16": ()
}

def initNotifications():
    now = datetime.datetime.now()
    for c, v in planning_sheet.items():
        if str(now.date()) == c:
            for d in v:
                daily_sheet.append(d)

def checkNotifications():
    data = 'Планы на сегодня: '
    for m in daily_sheet:
        data += str(m) + '. '
    
    if len(daily_sheet) == 0:
        data = 'На сегодня нет запланированных дел!'

    return data