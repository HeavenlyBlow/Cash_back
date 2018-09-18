# -*- coding: utf-8 -*-
import config
import telebot
import markups as m
import datetime
import database as db
 # import InformationOutputManager
from DataBasssee import mySQL
from InformationOutputManager import information_request, return_name, return_point, return_error, insert_information_registration
from Math_procent import points_value

bot = telebot.TeleBot(config.token)
global money, new_proc
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


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    console("/start", message)
    # bot.send_message(chat_id, text="/start", reply_markup=m.start_markup)
    msg1 = bot.send_message(chat_id, '''\U0000270CЗдравствуйте.\U0000270C
Вас приветствует кэш-бэк сервис - ********.''' + "\nВведите номер телефона в формате \"70000000000 или 80000000000\" \nСейчас процент: " + str(
        db.proc), reply_markup=m.markup_change_proc)
    # if(regs == False):
    #     bot.register_next_step_handler(msg1, handle_message)


@bot.message_handler(commands=['reg'])
def registrations_main(message):
    global regs, name, points, number

    if regs == False:
        clear_registration()

    regs = True

    try:
        if (name != ""):
            if (number != ""):

                points = points_value(int(message.text), db.proc)
                # Отправляем данные в базу данных

                if insert_information_registration(number, name, points) is True:
                    bot.send_message(message.chat.id, "Успешно!", reply_markup=m.markup_start)

                else:
                    bot.send_message(message.chat.id, "Уже зарегистрирован", reply_markup=m.markup_start)
                regs = False

    except:
        bot.send_message(message.chat.id, "Ошибка",reply_markup=m.markup_start)
        regs = False

    try:
        if (name != ''):
            if (regs is True):
                if (int(message.text) >= 79000000000) & (int(message.text) <= 89999999999):
                    in_number(message.text)
                    next_steep = bot.send_message(message.chat.id, "Введите сумму")
                    bot.register_next_step_handler(next_steep, registrations_main)

    except:
        pause = bot.send_message(message.chat.id, "Повторите ввод номера")
        bot.register_next_step_handler(pause, registrations_main)

    try:
        if (number == ''):
            if (regs is True):
                in_name(message.text)
                next_steep = bot.send_message(message.chat.id, "Введите номер телефона")
                bot.register_next_step_handler(next_steep, registrations_main)
    except:
        pause = bot.send_message(message.chat.id, "Повторите ввод имени")
        bot.register_next_step_handler(pause, registrations_main)


def clear_registration():
    global regs, name, points, number
    name = ''
    number = ''
    points = 0


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
    if is_int(message.text):
        points = points_value(message.text, db.proc)
        db.amount += points
        bot.send_message(chat_id, "Добавлено " + str(points) + " бонусов.\nТеперь баланс: " + str(db.amount),
                         reply_markup=m.markup_start)
    else:
        bot.send_message(chat_id, "Количество добавляемых баллов должно быть числом")
        bot.register_next_step_handler(message, add_points_two)


def in_point(message):
    global points
    points = int(message)


def in_name(message):
    global name
    name = message


def in_number(message):
    global number
    number = message


# def dispather(message):
#     global regs, num, name, number, points, stage
#     # Алгоритм регистрации
#     if (regs is True):
#
#         # while regs == False:
#             if (name != ''):
#                 if (number != ''):
#                     points = int(message.text)
#                     bot.send_message(message.chat.id, "Заносим в базу данных")
#                     db_work = mySQL(config.database_neme)
#                     # Отправляем данные в базу данных
#                     if db_work.registration(number, name, points) is True:
#                         bot.send_message(message.chat.id, "Успешно!")
#
#                         regs = False
#                     #     TODO не забыть отбработку ошибки регистрации
#
#                     else:
#                         bot.send_message(message.chat.id, "Уже зарегистрирован")
#                         regs = False
#
#                 # Если регистрация закончена закрываем бд
#                 if (regs is False):
#                     db_work.close()
#
#             # Если имя и номер не пустые то значит отправили баллы, можно делать запрос
#             #  Установка номера телефона если регистрация еще идет
#             if (name != ''):
#                 if (regs is True):
#                     if (int(message.text) >= 79000000000) & (int(message.text) <= 89999999999):
#                         number = message.text
#                         bot.send_message(message.chat.id, "Введите количество баллов")
#
#                     else:
#                         bot.send_message(message.chat.id, "Формат не поддерживается")
#                         regs = False
#
#             # Устанавливает имя если номер пустой и регистрация идет
#             if (number == ''):
#                 if (regs is True):
#                     if message.text != '':
#                         name = message.text
#                         bot.send_message(message.chat.id, "Введите номер телефона")
#                     else:
#                         bot.send_message(message.chat.id, "Имя не введено")



def handle_message(message):
    if (regs == False):
        chat_id = message.chat.id
        number = message.text
        information_request(number)
        if return_error() == False:
            bot.send_message(chat_id,"Информация о клиенте:\n\n" + "Имя:  " + return_name() + "\nНомер:  " + str(
                number) + "\n\nБаланс:  " + str(
                return_point()) , reply_markup=m.markup_change_points)
        else:
            bot.send_message(chat_id, "Номер " + number + " не зарегистрирован", reply_markup= m.markup_in_number)


def text_handler(message):
    console(message.text, message)
    chat_id = message.chat.id
    if message.text == "Помощь":
        bot.send_message(chat_id, "Тут будет помощь")
    else:
        bot.send_message(chat_id, "Команда не распознана")


def newproce(message):
    chat_id = message.chat.id
    if is_int(message.text) == True:
        db.proc = message.text
        bot.send_message(chat_id, "Процент изменен.\nНовый процент: " + db.proc, reply_markup=m.markup_start)
    elif message.text == "/start":
        bot.register_next_step_handler(message, start_handler)
    else:
        bot.send_message(chat_id, "Процент должен быть числом")
        bot.register_next_step_handler(message, newproce)


def np_info(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, "Новый процент: ")


@bot.callback_query_handler(func=lambda call: True)
def callback_key(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "input_number":
        try:
            mess = bot.edit_message_text("Введите номер телефона", chat_id, message_id)
            bot.register_next_step_handler(mess, handle_message)

        except:
            print("Ошибка ввода номер")
            return
    if call.data == "reg":
        try:

            mag1 = bot.edit_message_text("Введите имя", chat_id, message_id)
            bot.register_next_step_handler(mag1, registrations_main)

        except:
            print("Ошибка рег")
            return
    if call.data == "change_proc":
        try:
            msg1 = bot.edit_message_text("Введите новый процент", chat_id, message_id)
            bot.register_next_step_handler(msg1, newproce)

        except:
            print("Ошибка в change_proc")
            return
    if call.data == "start":
        try:
            bot.edit_message_text(
                '''\U0000270CЗдравствуйте.\U0000270C\nВас приветствует кэш-бэк сервис - ********.''' + "\nВведите номер телефона в формате \"70000000000 или 80000000000\" \nСейчас процент: " + str(
                    db.proc), chat_id, message_id, reply_markup=m.markup_change_proc)
        except:
            print("Ошибка в start")
            return
    if call.data == "add_points":
        try:
            msg1 = bot.edit_message_text("Введите сумму покупки", chat_id, message_id)
            bot.register_next_step_handler(msg1, add_points_two)
        except:
            print("Ошибка в add_points")
    if call.data == "sub_points":
        try:
            db.amount = 0
            bot.edit_message_text("Баланс теперь: " + str(db.amount), chat_id, message_id, reply_markup=m.markup_start)
        except:
            print("Ошибка в sub_points")


if __name__ == '__main__':
    bot.polling(none_stop=True)
