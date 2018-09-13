# _*_ coding: utf-8 _*_

    #     TODO Обвязать исключениями все методы
import sqlite3

class mySQL:
    # Инициализация класса бд, установка соединение и запуск курсора
    def __init__(self, database):
        self.connect = sqlite3.connect(database)
        self.cursor = self.connect.cursor()

    #    Метод регистрации возращает Тру(если вставка выполнена) или Фолс(если сработало исключение)
    def registration(self, number, name, points):
        try:
            with self.connect:
                self.cursor.execute("INSERT INTO Message VALUES (?,?,?)", (number,name,points,))
                return True
        except sqlite3.IntegrityError:
            return False

    #     Закрытие соединения с базой данных
    def close(self):
        self.connect.close()

    # Метод получения инфорации по номера возращает строки из бд, или не найдено
    def get_information(self, number):
        try:
            with self.connect:
                return self.cursor.execute("SELECT * FROM Message WHERE number = ?", (number,)).fetchall()[0]
        except IndexError:
            return "Не найдено"
