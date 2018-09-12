# -*- coding: utf-8 -*-
import config
import telebot
import markups as m
import datetime
import database as db
import re

bot = telebot.TeleBot(config.token)
global money,new_proc
money = 0

print("   Дата    |   Время  |  user_id  |  Команда")


def console(text, message):
    chat_id = message.chat.id
    print(str(datetime.datetime.fromtimestamp(message.date).strftime('%d.%m.%Y')) + " | " + str(
        datetime.datetime.fromtimestamp(message.date).strftime('%H:%M:%S')) + " | " + str(chat_id) + " | " + text)

def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    console("/start",message)
    bot.send_message(chat_id,
                    '''\U0000270CЗдравствуйте.\U0000270C
Вас приветствует кэш-бэк сервис - ********.''', reply_markup=m.start_markup)
    bot.send_message(chat_id, "Сейчас процент: " + str(db.proc) + "\nДля установки процента нажмите: /set_proc\nВведите номер телефона в формате \"+12345678901\"")

@bot.message_handler(commands=['set_proc'])
def set_proc(message):
    chat_id = message.chat.id
    msg1 = bot.send_message(chat_id, "Введите новый процент")

    if msg1.text == "/start":
        bot.register_next_step_handler(msg1,start_handler)
    else:
        bot.register_next_step_handler(msg1, newproce)

@bot.message_handler(regexp="\+ *")
def handle_message(message):
    chat_id=message.chat.id
    number = message.text
    number_in_db = True
    if number_in_db == True:
        msg = bot.send_message(chat_id, "Номер:\n" + str(number) + "\n\nБаланс:\n" + str(db.amount) + "\nЧто делать с баллами?", reply_markup=m.amount_markup)
        bot.register_next_step_handler(msg,change_points)
    else:
        bot.send_message(chat_id, "Номер " + number + " не зарегистрирован")

def change_points(message):
    chat_id=message.chat.id
    if message.text=="/start":
        bot.register_next_step_handler(message,start_handler)
    else:
        if message.text == "Добавить":
            msg = bot.send_message(chat_id, "Сколько добавить?")
            bot.register_next_step_handler(msg, add_points_two)
        elif message.text == "Обнулить":
            db.amount=0
            bot.send_message(chat_id,"Баланс теперь: " + str(db.amount))

def add_points_two(message):
    chat_id = message.chat.id
    if isint(message.text):
        db.amount = db.amount + int(message.text)
        bot.send_message(chat_id,"Добавлено " + str(message.text) + " бонусов.\nТеперь баланс: " + str(db.amount))
    else:
        bot.send_message(chat_id, "Количество добавляемых баллов должно быть числом")
        bot.register_next_step_handler(message,add_points_two)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    console(message.text, message)
    chat_id = message.chat.id
    if message.text == "Помощь":
        bot.send_message(chat_id, "Тут будет помощь")
    else:
        bot.send_message(chat_id, "Команда не распознана")

def newproce(message):
    chat_id=message.chat.id
    if isint(message.text) == True:
        db.proc=message.text
        bot.send_message(chat_id,"Процент изменен.\nНовый процент: " + db.proc)
    elif message.text=="/start":
        bot.register_next_step_handler(message,start_handler)
    else:
        bot.send_message(chat_id,"Процент должен быть числом2")
        bot.register_next_step_handler(message, newproce)

def np_info(message):
    chat_id=message.chat.id

    bot.send_message(chat_id,"Новый процент: ")


if __name__ == '__main__':
    bot.polling(none_stop=True)
