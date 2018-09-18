from config import database_neme
from DataBasssee import mySQL

# TODO Этот класс должен принимать строку с бд, обрабаытывать ее и формировать сообщение на вывод




name = ''
point = ''
error_request = False


# Метод получения инфорации с бд по номеру
def information_request(number):
    global name, point, error_request

    # Установка соединения
    db_worker = mySQL(database_neme)
    str = db_worker.get_information(number)
    db_worker.close()

    # Деление строки по переменным
    if (str != 'Не найдено'):
        print("найдено")
        k = 0
        error_request = False
        for i in str:
            if k == 1:
                name = i
            elif k == 2:
                point = i
            k += 1
    else:
        error_request = True
        print("ошибка")


def insert_information_registration(number,name,points):
    db_worker = mySQL(database_neme)

    if db_worker.registration(number, name, points) is True:
        db_worker.close()
        return True
    else:
        db_worker.close()
        return False






# def update_point():
#     db_worker = mySQL(database_neme)
#
#     if







def return_name():
    global name
    return name

def return_point():
    global point
    return point
def return_error():
    global error_request
    return error_request

# TODO Если Лешику не нужен номер то слует изменить цикл


