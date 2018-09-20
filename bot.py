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
global temp
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
    bot.send_message(message.chat.id,"Бот запущен",reply_markup=m.first_markup)
    handler_start(message)
    # if(regs == False):
    #     bot.register_next_step_handler(msg1, handle_message)

# Добавлено создание пользовательской таблицы и забивание времени
@bot.message_handler(commands=['reg'])
def registrations_main(message):
    global regs, name, points, number
    if message.text == "В главное меню":
        start_handler(message)
        regs = False
        return
    if regs == False:
        clear_registration()

    regs = True

    try:
        if (name != ""):
            if (number != ""):

                points = points_value(int(message.text), db.proc)
                # Отправляем данные в базу данных

                str_number = io_manager.number_processing(number)

                add_id = 1
                if io_manager.set_information_for_registration(str_number, name, points, add_id) is True:

                    # Создание пользовательской таблицы и забивание времени
                    io_manager.create_user_table(str_number)
                    # Записываем дату, время, баллы в таблицу индификатор которой время
                    io_manager.set_information_in_user_table(add_id, str_number, str(
                        datetime.datetime.fromtimestamp(message.date).strftime('%d.%m.%Y')), str(
                        datetime.datetime.fromtimestamp(message.date).strftime('%H:%M:%S')), points)

                    bot.send_message(message.chat.id, "Успешно!")

                else:
                    bot.send_message(message.chat.id, "Уже зарегистрирован")
                regs = False

    except:
        bot.send_message(message.chat.id, "Ошибка регистрации")
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

#Обработка кнопки "В главное меню"
@bot.message_handler(func = lambda message: message.text =="В главное меню")
def handler_start(message):
    chat_id = message.chat.id
    console("В главное меню", message)
    # bot.send_message(chat_id, text="/start", reply_markup=m.start_markup)
    msg1 = bot.send_message(chat_id, '''\U0000270CЗдравствуйте.\U0000270C
    Вас приветствует кэш-бэк сервис - ********.''' + "\nВведите номер телефона в формате \"70000000000 или 80000000000\" \nСейчас процент: " +
                            str(io_manager.get_percent()), reply_markup=m.markup_change_proc)



# Отчистка полей для регистрации
def clear_registration():
    global regs, name, points, number
    name = ''
    number = ''
    points = 0

# Определитель инта вынесен в инфор. менеджер
def add_points_two(message):
    chat_id = message.chat.id
    if message.text == "В главное меню":
        start_handler(message)
        return
    if io_manager.is_int(message.text):

        points = points_value(int(message.text), io_manager.get_percent())
        db_point = points + io_manager.return_point()

        # получение обработанного номера без 1 символов
        str_number = io_manager.return_number()

        io_manager.update_point(str_number, str(
                        datetime.datetime.fromtimestamp(message.date).strftime('%d.%m.%Y')), str(
                        datetime.datetime.fromtimestamp(message.date).strftime('%H:%M:%S')),
                                str(db_point))

        bot.send_message(chat_id, "Добавлено " + str(points) + " бонусов.\nТеперь баланс: " + str(db_point),
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
    if message.text == "В главное меню":
        handler_start(message)
        return
    if (regs == False):
        chat_id = message.chat.id
        number = message.text

        str_number = io_manager.number_processing(number)

        io_manager.information_request(str_number)
        if io_manager.return_error() == False:
            bot.send_message(chat_id,
                             "Информация о клиенте:\n\n" + "Имя:  " + io_manager.return_name() + "\nНомер:  " +
                                 io_manager.return_number() + "\n\nБаланс:  " +
                                 str(io_manager.return_point()), reply_markup=m.markup_change_points)
        else:
            bot.send_message(chat_id, "Номер " + number + " не зарегистрирован", reply_markup=m.markup_in_number)

@bot.message_handler(commands=["stop"])
def bot_stop(message):
    bot.stop_bot()

#Обработка посторонних сообщений
@bot.message_handler(content_types="text")
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
    if message.text == "В главное меню":
        handler_start(message)
        return
    elif (io_manager.is_int(message.text) == True):

        if (int(message.text) >= 0) & (int(message.text) <= 10):
            db.proc = message.text

            if io_manager.update_percent(int(message.text)) is True:
                bot.send_message(chat_id, "Процент изменен.\nНовый процент: " + db.proc)

        else:
            bot.send_message(chat_id, "Процент не должен быть выше 10")
            bot.register_next_step_handler(message, new_percent)


    else:
        bot.send_message(chat_id, "Процент должен быть числом")
        bot.register_next_step_handler(message, new_percent)


def np_info(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Новый процент: ")

#Обработка кнопок
@bot.callback_query_handler(func=lambda call: call.data != "change_proc")
def callback_key(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    #Обработка кнопки показа последних 10 действий
    if call.data == "history":
        pass
        #bot.edit_message_text(,call.message.chat.id,call.message.message_id)


    if call.data == "change_proc":
        try:
            msg1 = bot.edit_message_text("Введите процент не превышающий 10", call.message.chat.id,
                                         call.message.message_id)
            print(msg1.text)
            bot.register_next_step_handler(msg1, new_percent)
        except:
            print("Ошибка change_proc")
            return


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
