# -*- coding: utf-8 -*-

from InformationManager import input_output_manager as io
from Log import logs
logs = logs()




# Переписан под класс чтобы не плодил io
class administrators:
    io_manager = io()
    admins = {}
    admin_name = {}
    # adminId =
    #
    main_admin_name = {339425291: 'AlexDev',
                       447165655: 'AndreyDev',
                       413940724: 'Alexey'}


    def reload_admin_list(self):
        # print("Обновление списка администраторов")
        self.io_manager.get_admins_request()
        self.admins.clear()
        temp = self.io_manager.id_admin
        k = 0
        for i in temp:
            o = self.io_manager.name_admin[k]
            m = int(self.io_manager.id_admin[k])

            self.admins[o] = m
            self.admin_name[m] = o
            k += 1

    def get_admin_name(self, chat_id):
        try:
            if self.main_admin_name.get(chat_id) != None:
                return self.main_admin_name.get(chat_id)

            elif self.admin_name.get(chat_id) != None:
                return self.admin_name.get(chat_id)

        except:
            logs.error_logs("Error in get_admin_name")
            return

    def check_main_admins(self, chat_id):
        try:
            for p in self.main_admin_name.keys():
                if p == chat_id:
                    return True
            return False
        except:
            logs.error_logs("Error in check_main_admins")
            return False



