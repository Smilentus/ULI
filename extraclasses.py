class SheetBlock(object):
    '''
    Описание блока расписания
    Содержит:
    Дата 
    Флаг 'Каждый день'
    Список уведомлений
    '''    
    def __init__(self, date):
        self.date = date
        self.everyDay = False
        self.notifications = []

    def addNotifications(self, time, text):
        self.notifications.append((time, text))

    def getNotifications(self):
        data = ''
        for n in self.notifications:
            data += 'На {} запланировано {}. '.format(n[0], n[1])
        return data
        