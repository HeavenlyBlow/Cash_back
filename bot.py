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
    bot.send_message(chat_id, text=".", reply_markup=m.start_markup)
    bot.send_message(chat_id, '''\U0000270CЗдравствуйте.\U0000270C
Вас приветствует кэш-бэк сервис - ********.''' + "\nВведите номер телефона в формате \"+12345678901\" \nСейчас процент: " + str(db.proc), reply_markup=m.markup_change_proc)



@bot.message_handler(regexp="\+ *")
def handle_message(message):
    chat_id=message.chat.id
    number = message.text
    number_in_db = True
    if number_in_db == True:
        bot.send_message(chat_id, "Номер:\n" + str(number) + "\n\nБаланс:\n" + str(db.amount) + "\nЧто делать с баллами?", reply_markup=m.markup_change_points)

    else:
        bot.send_message(chat_id, "Номер " + number + " не зарегистрирован")



def add_points_two(message):
    chat_id = message.chat.id
    if isint(message.text):
        db.amount = db.amount + int(message.text)
        bot.send_message(chat_id,"Добавлено " + str(message.text) + " бонусов.\nТеперь баланс: " + str(db.amount), reply_markup=m.markup_start)
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
        bot.send_message(chat_id,"Процент изменен.\nНовый процент: " + db.proc, reply_markup=m.markup_start)
    elif message.text == "/start":
        bot.register_next_step_handler(message,start_handler)
    else:
        bot.send_message(chat_id,"Процент должен быть числом")
        bot.register_next_step_handler(message, newproce)

def np_info(message):
    chat_id=message.chat.id

    bot.send_message(chat_id,"Новый процент: ")

@bot.callback_query_handler(func=lambda call: True)
def callback_key(call):
    chat_id=call.message.chat.id
    message_id=call.message.message_id
    if call.data == "change_proc":
        try:
            # set_proc(call.message)
            msg1 = bot.edit_message_text("Введите новый процент",chat_id, message_id)
            bot.register_next_step_handler(msg1, newproce)

        except:
            print("Ошибка в change_proc")
            return
    if call.data == "start":
        try:
            bot.edit_message_text('''\U0000270CЗдравствуйте.\U0000270C\nВас приветствует кэш-бэк сервис - ********.''' +"\nВведите номер телефона в формате \"+12345678901\" \nСейчас процент: " + str(db.proc),chat_id, message_id, reply_markup=m.markup_change_proc)
        except:
            print("Ошибка в start")
            return
    if call.data == "add_points":
        try:
            msg1 = bot.edit_message_text("Сколько добавить?",chat_id,message_id)
            bot.register_next_step_handler(msg1, add_points_two)
        except:
            print("Ошибка в add_points")
    if call.data == "sub_points":
        try:
            db.amount = 0
            bot.edit_message_text("Баланс теперь: " + str(db.amount), chat_id,message_id,reply_markup=m.markup_start)
        except:
            print("Ошибка в sub_points")


if __name__ == '__main__':
    bot.polling(none_stop=True)
