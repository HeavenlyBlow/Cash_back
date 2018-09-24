# _*_ coding: utf-8 _*_

#     TODO Обвязать исключениями все методы
import sqlite3


class mySQL:
    # Инициализация класса бд, установка соединение и запуск курсора
    def __init__(self, database):
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()

    #    Метод регистрации возращает Тру(если вставка выполнена) или Фолс(если сработало исключение)
    def registration(self, number, name, points, add_id):
        try:
            with self.connect:
                self.cursor.execute("INSERT INTO Message VALUES (?,?,?,?)", (number, name, points, add_id,))
                return True
        except sqlite3.IntegrityError:
            return False

    #     Закрытие соединения с базой данных
    def close(self):
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
                return self.cursor.execute("SELECT * FROM Message WHERE number = ?", (number,)).fetchall()[0]
        except IndexError:
            return "Не найдено"

    def create_user_table(self, number):
        try:
            with self.connect:
                self.cursor.execute(
                """CREATE TABLE '""" + number + """' (id_add int UNIQUE, Date text,time text, point int)""")
        except:
            print("Ошибка в create_user_table")

    def delete_information_from_list_admins(self, admin_name):
        with self.connect:
            self.cursor.execute("DELETE FROM admins WHERE admin_name = ?", (admin_name,))
            return True

    def set_information_in_list_admins(self, user_id, admin_name):
        with self.connect:
            self.cursor.execute("INSERT INTO admins VALUES (?,?)", (str(user_id), admin_name,))
            return True

    def set_information_in_user_table(self, number, date, time, point, id_add):
        try:
            with self.connect:
                self.cursor.execute("""INSERT INTO '""" + number + """' VALUES (?,?,?,?)""", (id_add, date, time, point,))
                return True
        except:
            print("Ошибка в db.set_information_in_user_table ")

    def get_information_in_user_table(self, number, id):
        try:
            with self.connect:
                return self.cursor.execute("""SELECT * FROM '""" + number + """' WHERE id_add = ?""", (id,)).fetchall()[0]

        except:
            return "Ошибка"

    def update_point(self, number, point, id_add):
        try:
            while self.connect:
                self.cursor.execute("""UPDATE Message SET point = ' """ + point + """ ', id_add = '""" + id_add + """' WHERE number = """ + number)
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
                return True
        except:
            print("Ошибка в update_percent")
            return False
