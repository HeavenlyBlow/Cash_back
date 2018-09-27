# -*- coding: utf-8 -*-


import datetime
def console(text, message):
    chat_id = message.chat.id
    date = str(datetime.datetime.fromtimestamp(message.date).strftime('%d.%m.%Y'))
    time = str(datetime.datetime.fromtimestamp(message.date).strftime('%H:%M:%S'))
    print(date + " | " + time + " | " + str(chat_id) + " | " + text)