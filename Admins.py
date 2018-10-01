# -*- coding: utf-8 -*-

from InformationManager import input_output_manager as io
from Log import logs
logs = logs()




# Переписан под класс чтобы не плодил io
class administrators:
    io_manager = io()
    admins = {}
    main_admins = {'Алексей': 339425291,
                   'Андрей': 447165655,
                   'Кастрюля': 467989150}
    admin_name = {}




    def reload_admin_list(self):
        # print("Обновление списка администраторов")
        self.io_manager.get_admins_request()
        self.admins.clear()
        temp = self.io_manager.id_admin
        k = 0
        for i in temp:
            #self.admins[self.io_manager.name_admin[k]] = int(self.io_manager.id_admin[k])
            o = self.io_manager.name_admin[k]
            m = int(self.io_manager.id_admin[k])

            self.admins[o] = m
            self.admin_name[m] = o
            k += 1

    def get_admin_name(self, chat_id):
        try:
            return self.admin_name.get(chat_id)
        except:
            logs.error_logs("Ошибка в get_admin_name")
            return

    def check_main_admins(self, chat_id):
        try:
            for p in self.main_admins.values():
                if p == chat_id:
                    return True
                else:
                    return False
        except:
            logs.error_logs("Ошибка в check_main_admins")
            return False



