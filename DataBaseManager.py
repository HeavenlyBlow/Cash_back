# -*- coding: utf-8 -*-

#     TODO Обвязать исключениями все методы
import sqlite3
from Log import logs
import sys

logs = logs()

class SQL:
    # Инициализация класса бд, установка соединение и запуск курсора
    def __init__(self, database):
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()

    #    Метод регистрации возращает Тру(если вставка выполнена) или Фолс(если сработало исключение)
    def registration(self, number, name, points, add_id):
        try:
            with self.connect:
                self.cursor.execute("INSERT INTO Users VALUES (?,?,?,?)", (number, name, points, add_id,))
                self.connect.commit()
                return True
        except :
            e = sys.exc_info()[1]
            logs.error_logs("Error of registration: " + str(number) + " " + str(points) + " " + str(add_id))
            logs.error_logs(str(e))
            return False
    def check_number(self,number):
        try:
            with self.connect:
                # SELECT EXISTS(SELECT number FROM Users WHERE number = ?)
                answer = self.cursor.execute("SELECT * FROM Users WHERE NUMBER = ?", (number,)).fetchall()
                if answer.__len__() == 0:
                    return True
                else:
                    return False
        except:
            logs.error_logs("Error in check_number")
            e = sys.exc_info()[1]
            logs.error_logs(str(e))
            return False

    #     Закрытие соединения с базой данных
    def __del__(self):
        self.connect.close()

    def get_admins(self):
        try:
            with self.connect:
                return self.cursor.execute("SELECT * FROM Admins").fetchall()
        except IndexError:
            logs.error_logs("Error in get_admins")
            e = sys.exc_info()[1]
            logs.error_logs(str(e))
            return "Не найдено"

    # Метод получения инфорации по номера возращает строки из бд, или не найдено
    def get_information(self, number):
        try:
            with self.connect:
                return self.cursor.execute("SELECT * FROM Users WHERE number = ?", (number,)).fetchall()[0]
        except IndexError:
            logs.error_logs("Error in get_information")
            e = sys.exc_info()[1]
            logs.error_logs(str(e))
            return "Не найдено"

    def delete_information_from_list_admins(self, admin_name):
        try:
            with self.connect:
                self.cursor.execute("DELETE FROM admins WHERE admin_name = ?", (admin_name,))
                self.connect.commit()
                return True

        except:
            logs.error_logs("Error in del_inforamtion_from_list_admins")
            e = sys.exc_info()[1]
            logs.error_logs(str(e))

    def set_information_in_list_admins(self, user_id, admin_name):
        try:
            with self.connect:
                self.cursor.execute("INSERT INTO admins VALUES (?,?)", (str(user_id), admin_name,))
                self.connect.commit()
                return True
        except:
            logs.error_logs("Error in set_information_in_list_admins")
            e = sys.exc_info()[1]
            logs.error_logs(str(e))

    def set_information_in_history(self, number, date, time, point, id_add):

        try:
            with self.connect:
                self.cursor.execute("""INSERT INTO History VALUES (?,?,?,?,?)""", (number, date, time, point, id_add,))
                self.connect.commit()
                return True
        except:
            logs.error_logs("Error in set_inforamteion_in_history")
            e = sys.exc_info()[1]
            logs.error_logs(str(e))


    def get_information_in_history(self, number, add_id):
        try:
            with self.connect:
                return self.cursor.execute("""SELECT * FROM History WHERE number = ? and id = ?""", (number, add_id,)).fetchall()[0]
        except:
            logs.error_logs("Error in get_inforamtion_in_history")
            e = sys.exc_info()[1]
            logs.error_logs(str(e))
            return "Ошибка"

    def update_point(self, number, point, id_add):
        try:
            while self.connect:
                self.cursor.execute("""UPDATE Users SET point = ' """ + point + """ ', id_add = '""" + id_add + """' WHERE number = """ + number)
                self.connect.commit()
                return True
        except:
            logs.error_logs("Error in update_point")
            e = sys.exc_info()[1]
            logs.error_logs(str(e))
            return False

    #         TODO НЕ забыть создать файл логирования

    def get_percent(self):
        try:
            with self.connect:
                return self.cursor.execute("SELECT * FROM Percent").fetchall()
        except:
            logs.error_logs("Error in  get_percent")
            e = sys.exc_info()[1]
            logs.error_logs(str(e))

    def update_percent(self, percent):
        try:
            with self.connect:
                self.cursor.execute("""UPDATE Percent SET percent = ?""", (percent,))
                self.connect.commit()
                return True
        except:
            logs.error_logs("Error in update_percent")
            e = sys.exc_info()[1]
            logs.error_logs(str(e))
            return False

