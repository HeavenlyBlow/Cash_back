#_*_ coding: utf-8 _*_

import telebot
import config
from DataBasssee import mySQL
import InformationManager
import datetime

# Укозатель регистрации для фильтрации сообщений
regs = False

number = ''
name = ''
points = 0



bot = telebot.TeleBot(config.token)

io_menedger = InformationManager

# displayShow.information_request(123) - Пример запроса к displayShow, где 123 номер



@bot.message_handler(commands=['reg'])
def registrations(message):
    global regs, name, points, number
    regs = True
    name = ''
    number = ''
    points = 0
    bot.send_message(message.chat.id, "Введите имя")



@bot.message_handler(content_types = ['text'])
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

                str_number = io_menedger.number_processing(number)

                # Отправляем данные в базу данных
                if db_work.registration(number, name, points) is True:
                    bot.send_message(message.chat.id, "Успешно!")
                    io_menedger.create_user_table(str_number)
                    io_menedger.set_information_in_user_table(str_number, str(
                        datetime.datetime.fromtimestamp(message.date).strftime('%d.%m.%Y')), str(
                        datetime.datetime.fromtimestamp(message.date).strftime('%H:%M:%S')), points)
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

                # if (int(message.text) >= 79000000000  & int(message.text) <= 89999999999 ):
                if (int(message.text) >= 79000000000):
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



if __name__ == '__main__':
    bot.polling(none_stop=True)
