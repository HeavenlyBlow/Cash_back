# -*- coding: utf-8 -*-
import config
import telebot
import markups as m
import datetime
import database as db
import InformationManager
from console import console
from CheckUser import check_user, get_key
import vars
from DataBasssee import mySQL
# from InformationOutputManager import information_request, return_name, return_point, return_error, insert_information_registration
from Math_procent import points_value

bot = telebot.TeleBot(config.token)
io_manager = InformationManager

money = 0
regs = False
number = ''
name = ''
points = 0
date = ''
time = ''

print("   Дата    |   Время  |  user_id  |  Команда")

# При старте делает запрос в бд, при повтороном старте, использует локальный процент
@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        if check_user(message.chat.id):
            print("Авторизация user - " + str(vars.accept_user) + " прошла успешно!")
            if vars.admin_is_main == True:
                bot.send_message(message.chat.id, "Запуск бота", reply_markup=m.first_markup_main_admin)
            else:
                bot.send_message(message.chat.id, "Запуск бота", reply_markup=m.first_markup)
            handler_start(message)
        else:
            bot.send_message(message.chat.id,
                             "У вас нет прав заходить сюда. \nСообщите администратору ваш ID = " + str(message.chat.id),
                             reply_markup=m.markup_delete)
    except:
        bot.send_message(message.chat.id,"Ошибка авторизации")

    # if(regs == False):
    #     bot.register_next_step_handler(msg1, handle_message)

# Добавлено создание пользовательской таблицы и забивание времени
@bot.message_handler(commands=['reg'])
def registrations_main(message):
    if check_user(message.chat.id):
        global regs, name, points, number
        if message.text == "В главное меню":
            start_handler(message)
            regs = False
            return
        elif message.text == "Администрирование":
            manage_admins(message)
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
                    next_steep = bot.send_message(message.chat.id,
                                                  "Введите номер телефона \nв формате 7---------- или 8----------")
                    bot.register_next_step_handler(next_steep, registrations_main)
        except:
            pause = bot.send_message(message.chat.id, "Повторите ввод имени")
            bot.register_next_step_handler(pause, registrations_main)
    else:
        bot.send_message(message.chat.id, "У вас нет прав заходить сюда")


#Обработка кнопки "В главное меню"
@bot.message_handler(func = lambda message: message.text == "В главное меню")
def handler_start(message):
    if check_user(message.chat.id):
        chat_id = message.chat.id
        console("В главное меню", message)
        bot.send_message(chat_id,'\U0001F44BПривет, ' + str(vars.accept_user) + '\U0001F44B\nТебя приветствует кэш-бэк сервис - ********\nСейчас процент: ' +
                                str(io_manager.get_percent()), reply_markup=m.markup_change_proc)
    else:
        bot.send_message(message.chat.id, "У вас нет прав заходить сюда")

#Обработка кнопки "Администрирование"
@bot.message_handler(func = lambda message: message.text == "Администрирование")
def manage_admins(message):
    if db.admins == {}:
        global print_admins
        print_admins = "Список администраторов пуст!"
    else:
        print_admins = "Список администраторов:\nАдминистратор | ID\n\n"
        for i in db.admins:
            print_admins += str(i) + "  |  " + str(db.admins.get(i)) + "\n"
    try:
        # Главный админ
        if check_user(message.chat.id) & vars.admin_is_main:
            bot.send_message(message.chat.id, text=print_admins, reply_markup=m.markup_manage_admins)
        else:
            bot.send_message(message.chat.id, "У вас нет прав заходить сюда")
    except:
        bot.send_message(message.chat.id,"Ошибка в определении администратора")



# Определитель инта вынесен в инфор. менеджер
def add_points_two(message):
    chat_id = message.chat.id
    if message.text == "В главное меню":
        start_handler(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
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

        bot.send_message(chat_id, "Добавлено " + str(points) + " бонусов.\nБаланс: " + str(db_point))
    else:
        bot.send_message(chat_id, "Количество добавляемых баллов должно быть числом")
        bot.register_next_step_handler(message, add_points_two)

def sub_points(message):
    chat_id = message.chat.id
    if message.text == "В главное меню":
        start_handler(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return
    if io_manager.is_int(message.text) is True:
        input_point = str(io_manager.how_much_to_sub_point(message.text))

        if io_manager.error_request is False:

            str_number = io_manager.return_number()
            io_manager.update_point(str_number, str(
                        datetime.datetime.fromtimestamp(message.date).strftime('%d.%m.%Y')), str(
                        datetime.datetime.fromtimestamp(message.date).strftime('%H:%M:%S')),
                                    input_point)

            bot.send_message(chat_id, "Списано " + message.text + " бонусов. \nБаланс:  " + input_point)
        else:
            bot.send_message(chat_id, "Сумма списания не должна превышать: " + io_manager.return_point())
            bot.register_next_step_handler(message, sub_points)

    else:
        bot.send_message(chat_id, "Количество списываемых баллов должно быть числом")
        bot.register_next_step_handler(message, add_points_two)


def handle_message(message):
    if check_user(message.chat.id):
        if message.text == "В главное меню":
            handler_start(message)
            return
        elif message.text == "Администрирование":
            manage_admins(message)
            return
        if (regs == False):
            chat_id = message.chat.id
            number = message.text

            str_number = io_manager.number_processing(number)

            io_manager.get_information_request(str_number)
            if io_manager.return_error() == False:
                bot.send_message(chat_id,
                                 "Информация о клиенте:\n\n" + "Имя:  " + io_manager.return_name() + "\nНомер:  " +
                                 io_manager.return_number() + "\n\nБаланс:  " +
                                 str(io_manager.return_point()), reply_markup=m.markup_change_points)
            else:
                bot.send_message(chat_id, "Номер " + number + " не зарегистрирован", reply_markup=m.markup_in_number)
    else:
        bot.send_message(message.chat.id,"У вас нет прав заходить сюда")


# Добавлена запись процента в бд
def new_percent(message):
    if check_user(message.chat.id):
        chat_id = message.chat.id
        if message.text == "В главное меню":
            handler_start(message)
            return
        elif message.text == "Администрирование":
            manage_admins(message)
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
    else:
        bot.send_message(message.chat.id,"У вас нет прав заходить сюда")


def np_info(message):
    if message.text == "В главное меню":
        handler_start(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return
    chat_id = message.chat.id
    bot.send_message(chat_id, "Новый процент: ")

def history(message):

    chat_id = message.chat.id
    if message.text == "В главное меню":
        start_handler(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return

    if io_manager.is_int(message.text) is True:
        operations = int(message.text)

        if (operations != 0):
            answer = io_manager.get_information_from_user_table(io_manager.return_number(), operations)
            bot.send_message(chat_id, answer)

        else:
            bot.send_message(chat_id, "Количество операций должно быть больше 0")
            bot.register_next_step_handler(message, history)

    else:
        bot.send_message(chat_id, "Количество операций должно быть числом")
        bot.register_next_step_handler(message, history)

#Ввод имени нового админа
def add_admin_name(message):
    global admin_name
    if message.text == "В главное меню":
        handler_start(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return
    try:
        admin_name = message.text
        msg = bot.send_message(message.chat.id,"Введите ID нового администратора")
        bot.register_next_step_handler(msg, add_admin_id)
    except:
        bot.send_message(message.chat.id,"Ошибка добавления")

#Ввод ид нового админа
def add_admin_id(message):
    global admin_name
    if message.text == "В главное меню":
        handler_start(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return
    try:
        admin_id = message.text
        db.admins[admin_name] = int(admin_id)
        print("Добавление администратора " + admin_name + ":" + admin_id)
        bot.send_message(message.chat.id,"Администратор " + admin_name + " добавлен!")
        manage_admins(message)
    except:
        bot.send_message(message.chat.id,"Ошибка добавления")

#Удаление админа
def delete_admin_name(message):
    global print_admins
    if message.text == "В главное меню":
        handler_start(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return
    try:
        if message.text in db.admins.keys():
            db.admins.pop(message.text)
            print("Удаление администратора " + message.text)
            bot.send_message(message.chat.id, "Администратор " + message.text + " удален!")
            manage_admins(message)
        else:
            bot.send_message(message.chat.id, "Администратора с таким именем нет.\n" + print_admins,reply_markup=m.markup_repeat_set_delete_admin)

    except:
        bot.send_message(message.chat.id, "Ошибка удаления")


#Обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_key(call):
    if check_user(call.message.chat.id):
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        #Добавление админа
        if call.data == "add_admin":
            name_new_admin = bot.edit_message_text("Введите имя нового администратора",call.message.chat.id,call.message.message_id)
            bot.register_next_step_handler(name_new_admin, add_admin_name)

        #Удаление админа
        if call.data == "delete_admin":
            name_delete_admin = bot.edit_message_text("Введите имя администратора, которого хотите удалить.\n" + print_admins,
                                                      call.message.chat.id,call.message.message_id)
            bot.register_next_step_handler(name_delete_admin, delete_admin_name)

        # Обработка кнопки показа последних 10 действий
        if call.data == "history":
            msg1 = bot.edit_message_text("Введите количество операций не превышающих " + str(io_manager.return_add_id())
                                         , call.message.chat.id, call.message.message_id)

            bot.register_next_step_handler(msg1, history)

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
                mess = bot.edit_message_text("Введите номер телефона \nв формате 7---------- или 8----------", chat_id,
                                             message_id)
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
                msg1 = bot.edit_message_text(
                    "Введите количество списываемых баллов не превышающих:  " + str(io_manager.return_point())
                    , chat_id, message_id)
                bot.register_next_step_handler(msg1, sub_points)
                # bot.edit_message_text("Баланс теперь: " + str(db.amount), chat_id, message_id, reply_markup=m.markup_start)
            except:
                print("Ошибка в sub_points")
    else:
        bot.send_message(call.message.chat.id,"У вас нет прав заходить сюда")


# Отчистка полей для регистрации
def clear_registration():
    global regs, name, points, number
    name = ''
    number = ''
    points = 0



def in_name(message):
    global name
    name = message


def in_number(message):
    global number
    number = message


def in_point(message):
    global points
    points = int(message)


try:
    if __name__ == '__main__':
        bot.polling(none_stop=True)
except:
    print("!!!!!!Ошибка цикла!!!!!!")
