#_*_ coding: utf-8 _*_

import telebot
import config
from InformationOutputManager import displayShow
from DataBasssee import mySQL

# Укозатель регистрации для фильтрации сообщений
regs = False

number = ''
name = ''
points = 0

bot = telebot.TeleBot(config.token)


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

                # Отправляем данные в базу данных
                if db_work.registration(number, name, points) is True:
                    bot.send_message(message.chat.id, "Успешно!")

                    regs = False

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



if __name__ == '__main__':
    bot.polling(none_stop=True)
