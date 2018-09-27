# _*_ coding: utf-8 _*_

#     TODO Обвязать исключениями все методы
import sqlite3


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
        except sqlite3.IntegrityError:
            print("Ошибка в registrations:" + str(number) + " " + str(name) + " " + str(points) + " " + str(add_id))
            return False
    def check_number(self,number):
        try:
            with self.connect:
                # SELECT EXISTS(SELECT number FROM Users WHERE number = ?)
                answer = self.cursor.execute("SELECT * FROM Users WHERE NUMBER = ?", (number,)).fetchall()
                if answer.__len__() == 0:
                    print("Номер не зарегистрирован")
                    return True
                else:
                    print("Номер зарегистрирован")
                    return False
        except:
            print("false")
            return False

    #     Закрытие соединения с базой данных
    def __del__(self):
        self.connect.close()

    def get_admins(self):
        try:
            with self.connect:
                return self.cursor.execute("SELECT * FROM Admins").fetchall()
        except IndexError:
            return "Не найдено"

    # Метод получения инфорации по номера возращает строки из бд, или не найдено
    def get_information(self, number):
        try:
            with self.connect:
                return self.cursor.execute("SELECT * FROM Users WHERE number = ?", (number,)).fetchall()[0]
        except IndexError:
            return "Не найдено"

    # def create_user_table(self, number):
    #     try:
    #         with self.connect:
    #             self.cursor.execute(
    #             """CREATE TABLE '""" + number + """' (id_add int UNIQUE, Date text,time text, point int)""")
    #     except:
    #         print("Ошибка в create_user_table")

    def delete_information_from_list_admins(self, admin_name):
        with self.connect:
            self.cursor.execute("DELETE FROM admins WHERE admin_name = ?", (admin_name,))
            self.connect.commit()
            return True

    def set_information_in_list_admins(self, user_id, admin_name):
        with self.connect:
            self.cursor.execute("INSERT INTO admins VALUES (?,?)", (str(user_id), admin_name,))
            self.connect.commit()
            return True

    def set_information_in_history(self, number, date, time, point, id_add):

        with self.connect:
            self.cursor.execute("""INSERT INTO History VALUES (?,?,?,?,?)""", (number, date, time, point, id_add,))
            self.connect.commit()
            return True

    # def get_information_in_history(self, number):
    #
    #     with self.connect:
    #         return self.cursor.execute("SELECT * FROM History WHERE number = ?", (number,)).fetchall()[0]


    # def set_information_in_user_table(self, number, date, time, point, id_add):
    #     with self.connect:
    #         print(number, date, time, point, id_add)
    #         self.cursor.execute("""INSERT INTO '""" + number + """' VALUES (?,?,?,?)""", (id_add, date, time, point,))



    def get_information_in_history(self, number, add_id):
        # try:
            with self.connect:
                return self.cursor.execute("""SELECT * FROM History WHERE number = ? and id = ?""", (number, add_id,)).fetchall()[0]
        # except:
        #     return "Ошибка"

    def update_point(self, number, point, id_add):
        try:
            while self.connect:
                self.cursor.execute("""UPDATE Users SET point = ' """ + point + """ ', id_add = '""" + id_add + """' WHERE number = """ + number)
                self.connect.commit()
                return True
        except:
            print("Ошибка в update_point")
            return False

    #         TODO НЕ забыть создать файл логирования

    def get_percent(self):
        try:
            with self.connect:
                return self.cursor.execute("SELECT * FROM Percent").fetchall()
        except:
            print("Ошибка в get_percent(скорее всего не нафден файл с таблицей)")

    def update_percent(self, percent):
        try:
            with self.connect:
                self.cursor.execute("""UPDATE Percent SET percent = ?""", (percent,))
                self.connect.commit()
                return True
        except:
            print("Ошибка в update_percent")
            return False

