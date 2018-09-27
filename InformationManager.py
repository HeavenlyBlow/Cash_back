# -*- coding: utf-8 -*-

from config import database_neme
from DataBaseManager import SQL


# Этот класс должен принимать строку с бд, обрабаытывать ее и формировать сообщение на вывод


class input_output_manager:

    name = ''
    point = ''
    number = ''
    add_id = ''
    error_request = False
    percent = 0
    is_first = True
    id_admin = []
    name_admin = []


    def get_admins_request(self):
        db_worker = SQL(database_neme)
        str = db_worker.get_admins()
        db_worker.__del__()
        # Деление строки по переменным
        if (str != 'Не найдено'):
            print("Found in get_admins_request")
            k = 0
            self.id_admin = []
            self.name_admin = []
            nmb_of_notes = 0
            self.error_request = False

            for note in str:
                for drop in note:
                    if k == 0:
                        self.id_admin.append(drop)
                        k += 1
                    elif k == 1:
                        self.name_admin.append(drop)
                        k += 1
                        nmb_of_notes += 1
                k = 0
        else:
            self.error_request = True
            print("no found in get_admins_request")

    # Метод получения инфорации с бд по номеру
    def get_information_request(self, number):

        # Установка соединения
        db_worker = SQL(database_neme)
        str = db_worker.get_information(number)
        db_worker.__del__()

        # Деление строки по переменным
        if (str != 'Не найдено'):
            print("Found in get_information_request")
            k = 0
            self.error_request = False
            for i in str:
                if k == 3:
                    self.add_id = i
                    return

                if k == 0:
                    self.number = i
                    k += 1

                elif k == 1:
                    self.name = i
                    k += 1
                else:
                    self.point = i
                    k += 1

        else:
            self.error_request = True
            print("No found in get_information_request")

    def get_information_from_history(self, number, operations):

        db_worker = SQL(database_neme)
        self.error_request = False
        add_id = self.add_id


        id = add_id - operations


        k = 0
        answer = "Информация по " + str(operations) + " последним операциям: \n\n Дата           |Время     |Баллы\n\n"

        if (id <= add_id):

            while id < add_id:
                prom_1 = db_worker.get_information_in_history(number, add_id)
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
            self.error_request = True

        return answer

    def delete_information_from_list_admins(self, admin_id):
        db_worker = SQL(database_neme)
        if db_worker.delete_information_from_list_admins(admin_id):
            db_worker.__del__()
            return True
        else:
            db_worker.__del__()
            return False

    def set_information_in_list_admins(self, user_id, admin_name):
        db_worker = SQL(database_neme)
        if db_worker.set_information_in_list_admins(user_id, admin_name):
            db_worker.__del__()
            return True
        else:
            db_worker.__del__()
            return False

    def set_information_in_history(self, id_add, number, date, time, point):
        db_worker = SQL(database_neme)
        if db_worker.set_information_in_history(number, date, time, point, id_add):
            db_worker.__del__()
            return True
        else:
            db_worker.__del__()
            return False

    def set_information_for_registration(self, number, name, points, add_id):
        db_worker = SQL(database_neme)

        if db_worker.registration(number, name, points, add_id) is True:
            db_worker.__del__()
            return True
        else:
            db_worker.__del__()
            return False

    def check_number(self, number):
        db_worker = SQL(database_neme)
        if db_worker.check_number(number) is True:
            db_worker.__del__()
            return True
        else:
            db_worker.__del__()
            return False


    def is_int(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def number_processing(self, number):
        int_num = int(number)
        number = str(int_num)

        return number[1:]


    # Принимает все в строке, бд принимаем нит
    def update_point(self, number, date, time, point):
        db_worker = SQL(database_neme)

        add_id = self.add_id + 1

        if db_worker.update_point(number, point, str(add_id)) is True:
            if db_worker.set_information_in_history(number, date, time, point, add_id) is True:
                db_worker.__del__()
                self.add_id += 1
                return True
        else:
            db_worker.__del__()
            return False

    def update_percent(self, per):

        db_worker = SQL(database_neme)

        if db_worker.update_percent(per) is True:
            self.percent = int(per)
            db_worker.__del__()
            return True
        else:
            db_worker.__del__()
            return False

    def how_much_to_sub_point(self, input_point):

        self.error_request = False
        int_input_point = int(input_point)
        db_point = self.point

        if (int_input_point == db_point):
            return 0

        elif (int_input_point > self.point):
            self.error_request = True

        if (int_input_point < self.point):
            return db_point - int_input_point

    # Метод получения процента, срабатывает только при первом включении
    # TODO Перенести этот метод в инициализацию
    def get_percent(self):

        if self.is_first is True:

            db_worker = SQL(database_neme)
            per = str(db_worker.get_percent())

            # Т.к из бд выходит список, проверяется 4 символ, если не равен , значит число = 10, иначе <10
            if per[3] == ",":
                self.percent = int(per[2])

            else:
                st = per[2] + per[3]
                self.percent = int(st)

            self.is_first = False
            db_worker.__del__()
            return self.percent

        else:
            return self.percent

