# -*- coding: utf-8 -*-
import config
import telebot
import markups as m
import datetime
import database as db
from DataBasssee import mySQL
from InformationOutputManager import information_request,return_name,return_point,error_request


bot = telebot.TeleBot(config.token)
global money,new_proc
money = 0
regs = False
number = ''
name = ''
points = 0

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
    msg1=bot.send_message(chat_id, '''\U0000270CЗдравствуйте.\U0000270C
Вас приветствует кэш-бэк сервис - ********.''' + "\nВведите номер телефона в формате \"70000000000 или 80000000000\" \nСейчас процент: " + str(db.proc), reply_markup=m.markup_change_proc)
    bot.register_next_step_handler(msg1,handle_message)

@bot.message_handler(commands=['reg'])
def registrations(message):
    global regs, name, points, number
    regs = True
    name = ''
    number = ''
    points = 0
    bot.send_message(message.chat.id, "Введите имя")


# @bot.message_handler(regexp="\+ *")
# def handle_message(message):
#     chat_id=message.chat.id
#     number = message.text
#
#     information_request(number)
#
#     if error_request == False:
#         bot.send_message(chat_id, "Имя: " + return_name() + "\nНомер:\n" + str(number) + "\n\nБаланс:\n" + str(return_point()) + "\nЧто делать с баллами?", reply_markup=m.markup_change_points)
#
#     else:
#         bot.send_message(chat_id, "Номер " + number + " не зарегистрирован")



def add_points_two(message):
    chat_id = message.chat.id
    if isint(message.text):
        db.amount = db.amount + int(message.text)
        bot.send_message(chat_id,"Добавлено " + str(message.text) + " бонусов.\nТеперь баланс: " + str(db.amount), reply_markup=m.markup_start)
    else:
        bot.send_message(chat_id, "Количество добавляемых баллов должно быть числом")
        bot.register_next_step_handler(message,add_points_two)


@bot.message_handler(content_types=['text'])
def dispather(message):
    global regs,num,name,number,points,stage
    # Алгоритм регистрации
    if (regs is True):

        # Если имя и номер не пустые то значит отправили баллы, можно делать запрос
        if (name != ''):
            if (number != ''):

                points = int(message.text)

                bot.send_message(message.chat.id, "Заносим в базу данных")
                db_work = mySQL(config.database_neme)

                # Отправляем данные в базу данных
                if db_work.registration(number, name, points) is True:
                    bot.send_message(message.chat.id, "Успешно!")

                    regs = False
                #     TODO не забыть отбработку ошибки регистрации

                else:
                    bot.send_message(message.chat.id, "Уже зарегистрирован")
                    regs = False
                # Если регистрация закончена закрываем бд
                if(regs is False):
                    db_work.close()

        # Установка номера телефона если регистрация еще идет
        if (name != ''):
            if(regs is True):
                if (int(message.text) >= 79000000000  & int(message.text) <= 89999999999 ):
                    number = message.text
                    bot.send_message(message.chat.id, "Введите количество баллов")

        # Устанавливает имя если номер пустой и регистрация идет
        if (number == ''):
            if(regs is True):
                if message.text != '':
                    name = message.text
                    bot.send_message(message.chat.id, "Введите номер телефона")
                else:
                    bot.send_message(message.chat.id, "Имя не введено")

def handle_message(message):
    chat_id = message.chat.id
    number = message.text

    information_request(number)

    if error_request == False:
        bot.send_message(chat_id, "Имя: " + return_name() + "\nНомер:\n" + str(number) + "\n\nБаланс:\n" + str(return_point()) + "\nЧто делать с баллами?", reply_markup=m.markup_change_points)

    else:
        bot.send_message(chat_id, "Номер " + number + " не зарегистрирован")

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
            bot.edit_message_text('''\U0000270CЗдравствуйте.\U0000270C\nВас приветствует кэш-бэк сервис - ********.''' +"\nВведите номер телефона в формате \"70000000000 или 80000000000\" \nСейчас процент: " + str(db.proc),chat_id, message_id, reply_markup=m.markup_change_proc)
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
