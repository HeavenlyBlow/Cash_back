from config import database_neme
from DataBasssee import mySQL

# TODO Этот класс должен принимать строку с бд, обрабаытывать ее и формировать сообщение на вывод

class displayShow:

    name = ''
    point = 0

    # Метод получения инфорации с бд по номеру
    def information_request(number):
        global name, point

        # Установка соединения
        db_worker = mySQL(database_neme)
        str = db_worker.get_information(number)
        db_worker.close()

        # Деление строки по переменным
        if (str != 'Не найдено'):

            for i in str:
                if i == 1:
                    name = str
                elif i == 2:
                    point = int(str)

    # TODO Если Лешику не нужен номер то слует изменить цикл


