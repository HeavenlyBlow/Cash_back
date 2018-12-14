# -*- coding: utf-8 -*-
import config
import telebot
import Markups as m
from datetime import datetime
import sys
from CheckUser import check_user, set_admins_objects
from InformationManager import input_output_manager as io
from ObjectManager import Buffer
from Admins import administrators
from MathProcent import points_value
from Log import logs
import time
import cherrypy

buffer = Buffer()
ad = administrators()
set_admins_objects(ad)
log = logs()

money = 0
regs = False
number = ''
name = ''
points = 0
usage_number = ""
input_number = ""
error_points = False



bot = telebot.TeleBot(config.token)

WEBHOOK_HOST = '54.37.239.19'
WEBHOOK_PORT = 80 # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = 'webhook_cer.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = 'webhook_pke.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)




class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
           raise cherrypy.HTTPError(403)



log.info_logs("START BOT")


# При старте делает запрос в бд, при повтороном старте, использует локальный процент
#Обработка сообщения /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    io_manager = io()
    buffer.set_buffer(message.chat.id, io_manager)
    ad.reload_admin_list()
    if check_user(message.chat.id):
        log.info_logs("User -  " + str(message.chat.id) + " was authorized")
        if ad.check_main_admins(message.chat.id) == True:
            bot.send_message(message.chat.id, "Запуск бота", reply_markup=m.first_markup_main_admin)
        else:
            bot.send_message(message.chat.id, "Запуск бота", reply_markup=m.first_markup)
        handler_start(message)
    else:
        buffer.del_buffer(message.chat.id)
        bot.send_message(message.chat.id,
                         "У вас нет прав заходить сюда. \nСообщите администратору ваш ID = " + str(message.chat.id),
                         reply_markup=m.markup_delete)


# Добавлено создание пользовательской таблицы и забивание времени
#Обработка регистрации
def registrations_main(message):
    global usage_number, regs, name, points, number, input_number, error_points
    io_manager = buffer.get_buffer(message.chat.id)
    if check_user(message.chat.id):
        if regs == False:
            log.info_logs(str(message.chat.id) + " started registration")
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
            if input_number != "":
                number = input_number
                name = message.text
                input_number = ""
                next = bot.send_message(message.chat.id, "Введите сумму")
                bot.register_next_step_handler(next, registrations_main)
                return

            if (name != ""):
                if (number != ""):

                    if (int(message.text) >= 10000) | (int(message.text) <= 1):
                        msg1 = bot.send_message(message.chat.id, "Сумма покупки не может быть больше 10000 и меньше 1!\nПовторите ввод")
                        bot.register_next_step_handler(msg1, registrations_main)
                        error_points = True

                    else:
                        error_points = False
                        points = points_value(int(message.text), io_manager.percent)

                        # Отправляем данные в базу данных

                        log.info_logs("Set amount: " + str(message.text) + " Points: " + str(points))
                        str_number = io_manager.number_processing(number)

                        add_id = 1

                        if io_manager.set_information_for_registration(str_number, name, points, add_id) is True:
                            # # Создание пользовательской таблицы и забивание времени
                            # io_manager.create_user_table(str_number)
                            # Записываем дату, время, баллы в таблицу индификатор которой время
                            io_manager.set_information_in_history(add_id, str_number, str(
                                datetime.fromtimestamp(message.date).strftime('%d.%m.%Y')), str(
                                datetime.fromtimestamp(message.date).strftime('%H:%M:%S')), points)

                            bot.send_message(message.chat.id,
                                             "Успешно!\n\nИмя: " + name + "\nНомер: " + str(number) +
                                             "\nБаллов: " + str(points) +
                                             "\n\nТекущий процент: " + str(io_manager.percent))
                            if (config.adminId and not ad.check_main_admins(message.chat.id)):
                                admin = ad.get_admin_name(message.chat.id)
                                sentText = 'Начисление:\n\n⚙️' + admin + ': добавил(а) ' + str(
                                points) + ' баллов\n☎️Номер: +7' + str_number + '\n📌Процент: ' + str(
                                io_manager.percent)
                                bot.send_message(config.adminId, sentText)
                            log.info_logs("Writing is successful")
                        regs = False


        except:
            log.error_logs("Error of registration: " + str(name) + "|" + str(number) + "|" + str(points))
            bot.send_message(message.chat.id, "Ошибка регистрации")
            regs = False

        try:
            if (name != ''):
                if (regs is True):
                    if(error_points is False):

                        str_number = io_manager.number_processing(message.text)
                        if io_manager.check_number(str_number) is False:
                            bot.send_message(message.chat.id, "Уже зарегистрирован")
                            usage_number = message.text
                            handle_message(message)
                            return
                        if ((int(message.text) >= 79000000000) & (int(message.text) <= 89999999999)):
                            in_number(message.text)
                            log.info_logs("Entered number: " + message.text)
                            next_steep = bot.send_message(message.chat.id, "Введите сумму")
                            bot.register_next_step_handler(next_steep, registrations_main)
                            return
                        else:
                            log.error_logs("Number is not correct: " + message.text)
                            msg1 = bot.send_message(message.chat.id, "Номер введен некорректно. Повторите ввод номера")
                            bot.register_next_step_handler(msg1, registrations_main)
                            return
        except:
            log.error_logs("Error in entered number")
            pause = bot.send_message(message.chat.id, "Повторите ввод номера")
            bot.register_next_step_handler(pause, registrations_main)
            e = sys.exc_info()[1]
            log.error_logs(str(e))
            return
        try:
            if (number == ''):
                if (regs is True):
                    in_name(message.text)
                    next_steep = bot.send_message(message.chat.id,
                                                  "Введите номер телефона \nв формате 7---------- или 8----------")
                    log.info_logs("Entered name for registration")
                    bot.register_next_step_handler(next_steep, registrations_main)
        except:
            log.error_logs("Error of input name")
            pause = bot.send_message(message.chat.id, "Повторите ввод имени")
            bot.register_next_step_handler(pause, registrations_main)
    else:
        bot.send_message(message.chat.id, "У вас нет прав заходить сюда")


# TODO Баг: если в чате есть сообщение в главное меню он не сможет его обработать так как нет никаких ссылок
# Обработка кнопки "В главное меню"
@bot.message_handler(func=lambda message: message.text == "В главное меню")
def handler_start(message):
    global check_history, check_sub_points, check_add_points, regs, input_number
    check_add_points = False
    check_sub_points = False
    check_history = False
    regs = False
    input_number = ""
    io_manager = buffer.get_buffer(message.chat.id)
    if ((check_user(message.chat.id)) & (io_manager != None)):
        chat_id = message.chat.id
        # console("В главное меню", message)
        bot.send_message(chat_id, '\U0001F44BПривет, ' + ad.get_admin_name(message.chat.id) + '\U0001F44B\n' +
                                '\nТебя приветствует кэш-бэк сервис \"apple_house18\"                   \n\n'
                                + '\U0001F4CCСейчас процент: ' +
                         str(io_manager.get_percent()), reply_markup=m.markup_change_proc)
    elif io_manager == None:
        bot.send_message(message.chat.id, "Бот не запущен!")
        start_handler(message)
    else:
        bot.send_message(message.chat.id, "У вас нет прав заходить сюда")


# Обработка кнопки "Администрирование"
@bot.message_handler(func=lambda message: message.text == "Администрирование")
def manage_admins(message):
    global print_admins
    io_manager = buffer.get_buffer(message.chat.id)
    ad.reload_admin_list()
    if ad.admins == {}:
        print_admins = "Список администраторов пуст!"
    else:
        print_admins = "Администраторы:\n" + "\U00002796"*9 + "\n ID                |  Имя\n\n"
        for i in ad.admins:
            print_admins += str(ad.admins.get(i)) + " |  " + str(i) + "\n"
            # print_admins += str(i) + "  |  " + str(ad.admins.get(i)) + "\n"
    try:
        # Главный админ
        if (check_user(message.chat.id) & (ad.check_main_admins(message.chat.id)) & (io_manager != None)):
            bot.send_message(message.chat.id, text=print_admins, reply_markup=m.markup_manage_admins)

        elif io_manager == None:
            bot.send_message(message.chat.id, "Бот не запущен")
            start_handler(message)

        else:
            bot.send_message(message.chat.id, "У вас нет прав заходить сюда")
    except:
        log.error_logs("Error in the administrator definition:" + str(message.chat.id))
        bot.send_message(message.chat.id, "Ошибка в определении администратора")


# Определитель инта вынесен в инфор. менеджер
#Добавление баллов
def add_points_two(message):
    global check_history, check_add_points, check_sub_points
    io_manager = buffer.get_buffer(message.chat.id)
    chat_id = message.chat.id
    if message.text == "В главное меню":
        start_handler(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return

    try:
        if ((io_manager.is_int(message.text)) & (check_add_points == False)):
            points = points_value(int(message.text), io_manager.percent)
            db_point = points + io_manager.point
            io_manager.point = db_point
            # получение обработанного номера без 1 символов
            str_number = io_manager.number

            io_manager.update_point(str_number, str(
                datetime.fromtimestamp(message.date).strftime('%d.%m.%Y')), str(
                datetime.fromtimestamp(message.date).strftime('%H:%M:%S')),
                                    str(db_point))
            bot.send_message(chat_id,"Данные обновлены для номера +7" + io_manager.number +"\n\n\U0001F4DDДобавлено " + str(points) +
                             " баллов\n\U0001F4B0Баланс: " + str(db_point)
                             + "\n\n\U0001F4CCТекущий процент: " +
                             str(io_manager.get_percent()), reply_markup=m.markup_to_info)
            if (config.adminId and not ad.check_main_admins(message.chat.id)):
                date = datetime.strftime(datetime.now(), '%d.%m.%Y')
                time = datetime.strftime(datetime.now(), '%H:%M:%S')
                admin = ad.get_admin_name(chat_id)
                sentText = 'Начисление:\n\n⚙️' + admin + ': добавил(а) ' + str(
                    points) + ' баллов\n☎️Номер: +7' + io_manager.number + '\n📌Процент: ' + str(io_manager.percent)
                bot.send_message(config.adminId, sentText)
                # Запись в бд строки об добавлении баллов
                # io_manager.save_update(time, date, admin, 'add', points, int(io_manager.number))

            log.info_logs(str(message.chat.id) + " add " + str_number + " points: " + str(points))

            return
        #Проверка на то, нажал ли пользователь кнопку "Назад", чтобы не выводить сообщения по два раза
        elif ((check_add_points == True) & ((check_history == False))):
            check_add_points = False
            check_history = False
            history(message)
        elif ((check_add_points == True) & ((check_sub_points == False))):
            check_add_points = False
            check_sub_points = False
            sub_points(message)
        elif (check_add_points == True):
            check_sub_points = False
            check_add_points = False
            check_history = False

        else:
            bot.send_message(chat_id, "Количество добавляемых баллов должно быть числом")
            bot.register_next_step_handler(message, add_points_two)

    except:
        bot.send_message(chat_id, "Ошибка в добавлении")
        e = sys.exc_info()[1]
        print(str(e))
        log.error_logs("Error in adding points: " + str(message.chat.id))

#Удаление баллов
def sub_points(message):
    global check_history, check_sub_points, check_add_points
    io_manager = buffer.get_buffer(message.chat.id)
    chat_id = message.chat.id
    if message.text == "В главное меню":
        start_handler(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return
    try:
        if io_manager.is_int(message.text) is True:
            input_point = str(io_manager.how_much_to_sub_point(message.text))
            # +1 делается от избавления бага при нажатии кнопки назад полсе добавления : Не обновлялась инфа о истории
            if ((io_manager.error_request is False) & (check_sub_points == False)):
                str_number = io_manager.number
                io_manager.update_point(str_number, str(
                    datetime.fromtimestamp(message.date).strftime('%d.%m.%Y')), str(
                    datetime.fromtimestamp(message.date).strftime('%H:%M:%S')), input_point)
                io_manager.point = int(input_point)
                bot.send_message(chat_id,"Данные обновлены для номера +7" + io_manager.number +"\n\n\U0001F4DDСписано " +
                                 message.text + " баллов\n\U0001F4B0Баланс: " + input_point,
                                 reply_markup=m.markup_to_info)
                if (config.adminId and not ad.check_main_admins(message.chat.id)):
                    date = datetime.strftime(datetime.now(), '%d.%m.%Y')
                    time = datetime.strftime(datetime.now(), '%H:%M:%S')
                    admin = ad.get_admin_name(chat_id)
                    sentText = 'Списание:\n\n⚙️' + admin + ': списал(а) ' + str(message.text) + ' баллов\n☎️Номер: +7' + io_manager.number
                    bot.send_message(config.adminId, sentText)
                    # Запись в бд строки об списании баллов
                    # io_manager.save_update(time, date, admin, 'sub', int(message.text), int(io_manager.number))
                log.info_logs(str(message.chat.id) + " sub " + str_number + " " + message.text + " points")
                return

            # Проверка на то, нажал ли пользователь кнопку "Назад", чтобы не выводить сообщения по два раза
            elif ((check_sub_points == True) & ((check_add_points == False))):
                check_sub_points = False
                check_add_points = False
                add_points_two(message)
            elif ((check_sub_points == True) & ((check_history == False))):
                check_sub_points = False
                check_history = False
                history(message)
            elif (check_sub_points == True):
                check_sub_points = False
                check_add_points = False
                check_history = False

            else:
                bot.send_message(chat_id, "Сумма списания не должна превышать: " + str(io_manager.point) + "\nВведите сумму списания повторно:")
                bot.register_next_step_handler(message, sub_points)
        else:
            bot.send_message(chat_id, "Количество списываемых баллов должно быть числом")
            bot.register_next_step_handler(message, add_points_two)
    except:
        log.error_logs("Error in sub_point")

#Вывод информации о номере
def handle_message(message):
    global usage_number, input_number
    io_manager = buffer.get_buffer(message.chat.id)
    chat_id = message.chat.id
    if check_user(message.chat.id):
        if message.text == "В главное меню":
            input_number = ""
            handler_start(message)
            return
        elif message.text == "Администрирование":
            input_number = ""
            manage_admins(message)
            return

        try:
            text = message.text
            if usage_number != "":
                text = usage_number
                usage_number = ""
            number = text
            str_number = io_manager.number_processing(number)
            io_manager.get_information_request(str_number)
            if io_manager.error_request == False:
                log.info_logs(str(message.chat.id) + " requested information about the number: " + io_manager.number)
                bot.send_message(chat_id,
                                 "Информация о клиенте:\n" + "\U00002796"*9 + "\n\U0001F464Имя:  " + io_manager.name + "\n\U0000260EНомер:  " +
                                 io_manager.number + "\n\U0001F4B0Баланс:  " +
                                 str(io_manager.point), reply_markup=m.markup_change_points)
            else:
                if (int(message.text) >= 79000000000) & (int(message.text) <= 89999999999):
                    bot.send_message(chat_id, "Номер " + number + " не зарегистрирован",
                                     reply_markup=m.markup_in_number)
                    input_number = number
                else:
                    msg = bot.send_message(chat_id, "Номер введен некорректно. Повторите ввод номера")
                    bot.register_next_step_handler(msg, handle_message)
        except:
            log.error_logs("Error in handler_message" + str(chat_id) + "|" + message.text)
            msg1 = bot.send_message(chat_id, "Номер введен некорректно. Повторите ввод номера")
            bot.register_next_step_handler(msg1, handle_message)
            return

    else:
        bot.send_message(message.chat.id, "У вас нет прав заходить сюда")


# Добавлена запись процента в бд
#Изменение процента
def new_percent(message):
    io_manager = buffer.get_buffer(message.chat.id)
    if check_user(message.chat.id):
        chat_id = message.chat.id
        if message.text == "В главное меню":
            handler_start(message)
            return
        elif message.text == "Администрирование":
            manage_admins(message)
            return
        elif (io_manager.is_int(message.text) == True):
            if (int(message.text) >= 0) & (int(message.text) <= 20):
                percent = message.text
            else:
                mes1 = bot.send_message(chat_id, "Процент не должен быть выше 20.\nВведите корректный процент")
                bot.register_next_step_handler(mes1, new_percent)
                return

            if io_manager.update_percent(int(message.text)) is True:
                bot.send_message(chat_id, "Процент изменен\U00002705")
                handler_start(message)
                log.info_logs(str(message.chat.id) + " set percent to " + str(percent))
        else:
            bot.send_message(chat_id, "Процент должен быть целым числом")
            bot.register_next_step_handler(message, new_percent)
    else:
        bot.send_message(message.chat.id, "У вас нет прав заходить сюда")


# TODO Вылетает с ошибкой если ввести количество записей больше 8
#Вывод истории изменений
def history(message):
    global check_history, check_sub_points, check_add_points
    io_manager = buffer.get_buffer(message.chat.id)
    chat_id = message.chat.id
    if message.text == "В главное меню":
        start_handler(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return

    if (io_manager.is_int(message.text) is True):
        operations = int(message.text)
        log.info_logs(str(message.chat.id) + " requested history")
        if ((operations != 0) & (check_history == False)):
            answer = io_manager.get_information_from_history(io_manager.number, operations)
            bot.send_message(chat_id, answer, reply_markup=m.markup_to_info)
            return
        # Проверка на то, нажал ли пользователь кнопку "Назад", чтобы не выводить сообщения по два раза
        elif ((check_history == True) & ((check_add_points == False))):
            check_history = False
            check_add_points = False
            add_points_two(message)
        elif ((check_history == True) & ((check_sub_points == False))):
            check_history = False
            check_sub_points = False
            sub_points(message)
        elif (check_history == True):
            check_sub_points = False
            check_add_points = False
            check_history = False

        else:
            bot.send_message(chat_id, "Количество операций должно быть больше 0")
            bot.register_next_step_handler(message, history)
    else:
        bot.send_message(chat_id, "Количество операций должно быть числом")
        bot.register_next_step_handler(message, history)


# Ввод имени нового админа
def add_admin_name(message):
    global admin_name
    io_manager = buffer.get_buffer(message.chat.id)
    if message.text == "В главное меню":
        handler_start(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return
    try:
        log.info_logs(str(message.chat.id) + " add admin: " + message.text)
        ad.reload_admin_list()
        admin_name = message.text
        if admin_name not in ad.admins.keys():
            msg = bot.send_message(message.chat.id, "Введите ID нового администратора")
            bot.register_next_step_handler(msg, add_admin_id)
        else:
            bot.send_message(message.chat.id, "Такое имя уже занято", reply_markup=m.markup_repeat_new_admin)
    except:
        log.error_logs("Error in add_admin_name: " + str(message.chat.id) + " entered " + admin_name)
        bot.send_message(message.chat.id, "Ошибка добавления")


# Ввод ид нового админа
def add_admin_id(message):
    global admin_name
    io_manager = buffer.get_buffer(message.chat.id)
    if message.text == "В главное меню":
        handler_start(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return
    try:
        admin_id = message.text
        io_manager.set_information_in_list_admins(int(admin_id), admin_name)
        # print("Adding an administrator: name=" + admin_name.encode('UTF-8') + ", ID=" + admin_id)
        bot.send_message(message.chat.id, "Администратор " + admin_name + " добавлен!")
        manage_admins(message)
    except ValueError:
        log.error_logs(str(message.chat.id) + " incorrectly entered a percent")
        bot.send_message(message.chat.id, "ID должно быть числом", reply_markup=m.markup_repeat_new_admin)
        e = sys.exc_info()[1]
        log.error_logs(str(e))


# Удаление админа
def delete_admin_name(message):
    global print_admins
    io_manager = buffer.get_buffer(message.chat.id)
    if message.text == "В главное меню":
        handler_start(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return
    ad.reload_admin_list()
    if message.text in ad.admins.keys():
        io_manager.delete_information_from_list_admins(message.text)
        bot.send_message(message.chat.id, "Администратор " + message.text + " удален!")
        log.info_logs(str(message.chat.id) + " delete admin: " + message.text)
        manage_admins(message)
    else:
        bot.send_message(message.chat.id, "Администратора с таким именем нет.\n" + print_admins,
                         reply_markup=m.markup_repeat_set_delete_admin)

def check_date(date):
    try:
        time.strptime(date, '%d.%m.%Y')
    except ValueError:
        date = 'Error'
    return date

def output_info(message):
    if message.text == "В главное меню":
        handler_start(message)
        return
    elif message.text == "Администрирование":
        manage_admins(message)
        return
    io_manager = buffer.get_buffer(message.chat.id)
    date = check_date(message.text)

    if date != 'Error':
        answer = io_manager.get_update(date)
        out = 'Вывод информации об операциях за ' + date + '\n' + '\U00002796' * 9 + '\n'
        if answer == []:
            bot.send_message(message.chat.id, date + ' не было операций', reply_markup=m.markup_another_day)
            return
        for data in answer:
            if data[4] == 'sub':
                out += '[' + data[1] + ']: ' + '\U00002796' + data[3] + ' списал ' + str(data[5]) + ' баллов для номера ' + str(data[6])
            else:
                out += '[' + data[1] + ']: ' + '\U00002795' + data[3] + ' добавил ' + str(data[5]) + ' баллов для номера ' + str(
                    data[6])
            out += '\n'
        bot.send_message(message.chat.id, out, reply_markup=m.markup_another_day)
    else:
        bot.send_message(message.chat.id, 'Дата введена некорректно!', reply_markup=m.markup_another_day)


# Обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_key(call):
    # Глобальные переменнеые нужно убирать, с ними работать не будет
    global print_admins, check_history, check_sub_points, check_add_points
    if check_user(call.message.chat.id):
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        io_manager = buffer.get_buffer(chat_id)

        if io_manager == None:
            bot.send_message(chat_id, "Бот не запущен")
            start_handler(call.message)
            return

        # Добавление админа
        if ((call.data == "add_admin") & (ad.check_main_admins(chat_id))):
            name_new_admin = bot.edit_message_text("Введите имя нового администратора", call.message.chat.id,
                                                   call.message.message_id)
            bot.register_next_step_handler(name_new_admin, add_admin_name)

        # Удаление админа
        if call.data == "delete_admin":
            name_delete_admin = bot.edit_message_text(
                "Введите имя администратора, которого хотите удалить.\n" + print_admins,
                call.message.chat.id, call.message.message_id)
            bot.register_next_step_handler(name_delete_admin, delete_admin_name)

        # Информация об изменениях количества баллов
        if call.data == "info":
            input_data = bot.edit_message_text(
                "Введите дату в формате ДД.ММ.ГГГГ для показа истории операций за выбранный день.",
                call.message.chat.id, call.message.message_id)
            bot.register_next_step_handler(input_data, output_info)

        #Нажатие на кнопку "Изменить процент"
        if call.data == "change_proc":
            try:
                msg19 = bot.edit_message_text("Введите процент не превышающий 20", call.message.chat.id,
                                              call.message.message_id)
                bot.register_next_step_handler(msg19, new_percent)
            except:
                log.error_logs("Error of button сhange_proc")
                return

        #Нажатие на кнопку "Ввести номер"
        if call.data == "input_number":
            try:
                mess = bot.edit_message_text("Введите номер телефона \nв формате 7---------- или 8----------", chat_id,
                                             message_id)
                bot.register_next_step_handler(mess, handle_message)
            except:
                log.error_logs("Error in button input_number")
                return

        #Нажатие на кнопку "Регистрация"
        if call.data == "reg":
            try:
                mag1 = bot.edit_message_text("Введите имя", chat_id, message_id)
                bot.register_next_step_handler(mag1, registrations_main)

            except:
                log.error_logs("Error in button reg")
                return

        # Обработка кнопки показа последних действий
        if call.data == "history":
            try:
                msg13 = bot.edit_message_text("Введите количество операций не превышающих " + str(io_manager.add_id),
                                              call.message.chat.id, call.message.message_id,
                                              reply_markup=m.markup_back_to_info)
                if (check_history == False):
                    bot.register_next_step_handler(msg13, history)

                check_history = False
            except:
                log.error_logs("Error in button history")

        #Нажатие на кнопку "Добавить"
        if call.data == "add_points":
            try:
                msg2 = bot.edit_message_text("Введите сумму покупки", chat_id, message_id,
                                             reply_markup=m.markup_back_to_info)
                if (check_add_points == False):
                    bot.register_next_step_handler(msg2, add_points_two)
                check_add_points = False
            except:
                log.error_logs("Error in button add_point")

        #Нажатие на кнопку "Списать"
        if call.data == "sub_points":
            try:
                msg3 = bot.edit_message_text(
                    "Введите количество списываемых баллов не превышающих  " + str(io_manager.point),
                    chat_id, message_id, reply_markup=m.markup_back_to_info)
                if (check_sub_points == False):
                    bot.register_next_step_handler(msg3, sub_points)
                check_sub_points = False
            except:
                log.error_logs("Error in button sub_points")

        #Нажатие на кнопку "Назад"
        if call.data == "back_to_info":
            bot.send_message(chat_id,
                             "Информация о клиенте:\n" + "\U00002796"*9 + "\n\U0001F464Имя:  " + io_manager.name + "\n\U0000260EНомер: " +
                             io_manager.number + "\n\U0001F4B0Баланс:  " +
                             str(io_manager.point), reply_markup=m.markup_change_points)
            check_history = True
            check_add_points = True
            check_sub_points = True
            bot.delete_message(chat_id, message_id)

        #Нажатие на кнопку "К информации о номере"
        if call.data == "to_info":
            bot.send_message(chat_id,
                             "Информация о клиенте:\n" + "\U00002796"*9 + "\n\U0001F464Имя:  " + io_manager.name + "\n\U0000260EНомер: " +
                             io_manager.number + "\n\U0001F4B0Баланс:  " +
                             str(io_manager.point), reply_markup=m.markup_change_points)
            bot.delete_message(chat_id, message_id)

    else:
        bot.send_message(call.message.chat.id, "У вас нет прав заходить сюда")


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

def main():
    bot.polling(none_stop=True)


bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})



#try:
#     if __name__ == '__main__':
#         main()
#except:
#     log.error_logs("Ошибка цикла!")
