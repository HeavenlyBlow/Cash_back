# -*- coding: utf-8 -*-
import config
import telebot
import markups as m
import datetime
import database as db
import InformationManager
from DataBasssee import mySQL
# from InformationOutputManager import information_request, return_name, return_point, return_error, insert_information_registration
from Math_procent import points_value

bot = telebot.TeleBot(config.token)
io_manager = InformationManager

# global money, new_proc

money = 0
regs = False
number = ''
name = ''
points = 0
date = ''
time = ''


print("   Дата    |   Время  |  user_id  |  Команда")


def console(text, message):
    chat_id = message.chat.id
    date = str(datetime.datetime.fromtimestamp(message.date).strftime('%d.%m.%Y'))
    time = str(datetime.datetime.fromtimestamp(message.date).strftime('%H:%M:%S'))
    print(date + " | " + time + " | " + str(chat_id) + " | " + text)


# При старте делает запрос в бд, при повтороном старте, использует локальный процент
@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    console("/start", message)
    # bot.send_message(chat_id, text="/start", reply_markup=m.start_markup)
    msg1 = bot.send_message(chat_id, '''\U0000270CЗдравствуйте.\U0000270C
Вас приветствует кэш-бэк сервис - ********.''' + "\nВведите номер телефона в формате \"70000000000 или 80000000000\" \nСейчас процент: " +
                            str(io_manager.get_percent()), reply_markup=m.markup_change_proc)
    # if(regs == False):
    #     bot.register_next_step_handler(msg1, handle_message)

# Добавлено создание пользовательской таблицы и забивание времени
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

                str_number = io_manager.number_processing(number)

                if io_manager.set_information_for_registration(str_number, name, points) is True:

                    # Создание пользовательской таблицы и забивание времени
                    io_manager.create_user_table(str_number)
                    # Записываем дату, время, баллы в таблицу индификатор которой время
                    io_manager.set_information_in_user_table(str_number, str(
                        datetime.datetime.fromtimestamp(message.date).strftime('%d.%m.%Y')), str(
                        datetime.datetime.fromtimestamp(message.date).strftime('%H:%M:%S')), points)

                    bot.send_message(message.chat.id, "Успешно!", reply_markup=m.markup_start)

                else:
                    bot.send_message(message.chat.id, "Уже зарегистрирован", reply_markup=m.markup_start)
                regs = False

    except:
        bot.send_message(message.chat.id, "Ошибка", reply_markup=m.markup_start)
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

# Отчистка полей для регистрации
def clear_registration():
    global regs, name, points, number
    name = ''
    number = ''
    points = 0

# Определитель инта вынесен в инфор. менеджер
def add_points_two(message):
    chat_id = message.chat.id
    if io_manager.is_int(message.text):
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


def handle_message(message):
    if (regs == False):
        chat_id = message.chat.id
        number = message.text
        io_manager.information_request(number)
        if io_manager.return_error() == False:
            bot.send_message(chat_id,
                             "Информация о клиенте:\n\n" + "Имя:  " + io_manager.return_name() + "\nНомер:  " + str(
                                 number) + "\n\nБаланс:  " + str(
                                 io_manager.return_point()), reply_markup=m.markup_change_points)
        else:
            bot.send_message(chat_id, "Номер " + number + " не зарегистрирован", reply_markup=m.markup_in_number)


def text_handler(message):
    console(message.text, message)
    chat_id = message.chat.id
    if message.text == "Помощь":
        bot.send_message(chat_id, "Тут будет помощь")
    else:
        bot.send_message(chat_id, "Команда не распознана")

# Добавлена запись процента в бд
def new_percent(message):
    chat_id = message.chat.id
    if (io_manager.is_int(message.text) == True):

        if (int(message.text) >= 0) & (int(message.text) <= 10):
            db.proc = message.text

            if io_manager.update_percent(int(message.text)) is True:
                bot.send_message(chat_id, "Процент изменен.\nНовый процент: " + db.proc, reply_markup=m.markup_start)

        elif message.text == "/start":
            bot.register_next_step_handler(message, start_handler)

        else:
            bot.send_message(chat_id, "Процент должен быть числом")
            bot.register_next_step_handler(message, new_percent)


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
            bot.register_next_step_handler(msg1, new_percent)

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
