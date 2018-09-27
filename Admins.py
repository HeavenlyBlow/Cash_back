from InformationManager import input_output_manager as io


# print("id0 = " + str(io.return_id_admin()[0]) +
#       "\nname0 = " + str(io.return_name_admin()[0]) +
#       "\nis main0 = " + str(io.return_main_admin()[0]) +
#       "\nid1 = " + str(io.return_id_admin()[1]) +
#       "\nname1 = " + str(io.return_name_admin()[1]) +
#       "\nis main1 = " + str(io.return_main_admin()[1])
#       )


# Переписан под класс чтобы не плодил io
class administrators:
    proc = 0
    io_manager = io()
    admins = {}
    main_admins = {'Алексей': 339425291,
                   'Андрей': 447165655,
                   'Кастрюля': 467989150}



    def reload_admin_list(self):
        print("Обновление списка администраторов")
        self.io_manager.get_admins_request()
        self.admins.clear()
        temp = self.io_manager.id_admin
        k = 0
        for i in temp:
            self.admins[self.io_manager.name_admin[k]] = int(self.io_manager.id_admin[k])
            k += 1






# main_admins = {'Алексей' : 339425291,
#                'Андрей' : 447165655,
#                'Кастрюля' : 467989150}
# admins = {}
# #Обновить переменную admins
# def reload_admin_list():
#     io.get_admins_request()
#     admins.clear()
#     temp = io.return_id_admin()
#     k = 0
#     for i in temp:
#         admins[io.return_name_admin()[k]] = int(io.return_id_admin()[k])
#         k += 1
#



