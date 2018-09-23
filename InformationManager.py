from config import database_neme
from DataBasssee import mySQL

# TODO Этот класс должен принимать строку с бд, обрабаытывать ее и формировать сообщение на вывод





name = ''
point = ''
num = ''
add_id = ''
error_request = False
percent = 0
is_first = True

def get_admins_request():
    global error_request, id_admin, name_admin
    db_worker = mySQL(database_neme)
    str = db_worker.get_admins()
    db_worker.close()
    # Деление строки по переменным
    if (str != 'Не найдено'):
        print("найдено")
        k = 0
        id_admin = []
        name_admin = []
        nmb_of_notes = 0
        error_request = False

        for note in str:
            for drop in note:
                if k == 0:
                    id_admin.append(drop)
                    k += 1
                elif k == 1:
                    name_admin.append(drop)
                    k += 1
                    nmb_of_notes += 1
            k = 0
    else:
        error_request = True
        print("не найдено админа")


# Метод получения инфорации с бд по номеру
def get_information_request(number):
    global name, point, error_request, num, add_id
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
            if k == 3:
                add_id = i
                return

            if k == 0:
                num = i
                k += 1

            elif k == 1:
                name = i
                k += 1
            else:
                point = i
                k += 1

    else:
        error_request = True
        print("не найдено")


def get_information_from_user_table(number, operations):
    global error_request
    db_worker = mySQL(database_neme)
    error_request = False
    add_id = return_add_id()
    id = add_id - operations

    k = 0
    answer = "Информация по " + str(operations) + " последним операциям: \n\n Дата           |Время     |Баллы\n\n"

    if (id <= add_id):

        while id < add_id:
            prom_1 = db_worker.get_information_in_user_table(number, add_id)
            if prom_1 != "Ошибка":
                add_id -= 1
                k = 0
                for i in prom_1:
                    if k == 1:
                        answer += str(i) + " | "

                    elif k == 2:
                        answer += str(i) + " |   "

                    if k == 3:
                        answer += str(i) + "\n"

                    k += 1
            else:
                return "Ошибка в базе данных"

    else:
        error_request = True

    return answer

def set_information_in_list_admins(user_id, admin_name):
    db_worker = mySQL(database_neme)
    if db_worker.set_information_in_list_admins(user_id, admin_name):
        db_worker.close()
        return True
    else:
        db_worker.close()
        return False

def set_information_in_user_table(id_add, number, date, time, point):
    db_worker = mySQL(database_neme)
    if db_worker.set_information_in_user_table(number, date, time, point, id_add):
        db_worker.close()
        return True
    else:
        db_worker.close()
        return False


def set_information_for_registration(number, name, points, add_id):
    db_worker = mySQL(database_neme)

    if db_worker.registration(number, name, points, add_id) is True:
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

    add_id = int(return_add_id()) + 1

    if db_worker.update_point(number, point, str(add_id)) is True:
        if db_worker.set_information_in_user_table(number, date, time, point, add_id) is True:
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


def how_much_to_sub_point(input_point):
    global error_request, point
    error_request = False
    int_input_point = int(input_point)

    if (int_input_point == point):
        point = 0
        return point

    elif (int_input_point > point):
        error_request = True
        return 0

    if (int_input_point < point):
        point -= int_input_point
        return point


# Метод получения процента, срабатывает только при первом включении
def get_percent():
    global is_first, percent

    if is_first is True:

        db_worker = mySQL(database_neme)
        per = str(db_worker.get_percent())

        # Т.к из бд выходит список, проверяется 4 символ, если не равен , значит число = 10, иначе <10
        if per[3] == ",":
            percent = int(per[2])

        else:
            st = per[2] + per[3]
            percent = int(st)

        is_first = False

        return percent

    else:
        return percent


def return_name_admin():
    global name_admin
    return name_admin

def return_id_admin():
    global id_admin
    return id_admin

def return_number():
    global num
    return num


def return_name():
    global name
    return name


def return_point():
    global point
    return point


def return_add_id():
    global add_id
    return add_id


def return_error():
    global error_request
    return error_request

# TODO Если Лешику не нужен номер то слует изменить цикл
