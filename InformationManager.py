from config import database_neme
from DataBasssee import mySQL

# TODO Этот класс должен принимать строку с бд, обрабаытывать ее и формировать сообщение на вывод


name = ''
point = ''
error_request = False
percent = 0
is_first = True

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


def set_information_in_user_table(number, date, time, point):
    db_worker = mySQL(database_neme)
    if db_worker.set_information_in_user_table(number, date, time, point):
        db_worker.close()
        return True
    else:
        db_worker.close()
        return False


def set_information_for_registration(number, name, points):
    db_worker = mySQL(database_neme)

    if db_worker.registration(number, name, points) is True:
        db_worker.close()
        return True
    else:
        db_worker.close()
        return False


def create_user_table(number):
    try:
        db_worker = mySQL(database_neme)
        db_worker.create_user_table(number)
        db_worker.close()

    except:
        print("Ошибка в create_point_bank")
        db_worker.close()



def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def number_processing(number):
    int_num = int(number)
    number = str(int_num)

    return number[1:]


def update_point(number, date, time, point):

    db_worker = mySQL(database_neme)
    if db_worker.update_point(number, date, time, point) is True:
        db_worker.close()
        return True
    else:
        db_worker.close()
        return False

def update_percent(per):
    global percent
    db_worker = mySQL(database_neme)

    if db_worker.update_percent(per) is True:
        percent = int(per)
        return True
    else:
        return False

def get_percent():
    global is_first, percent

    if is_first is True:

        db_worker = mySQL(database_neme)

        per = str(db_worker.get_percent())
        percent = int(per[2])

        is_first = False
        return percent

    else: return percent



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
