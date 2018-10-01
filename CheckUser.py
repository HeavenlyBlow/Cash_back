# -*- coding: utf-8 -*-
ad = ''

def check_user(id):
    try:
        for j in ad.main_admins.values():
            if j == id:
                return True
        for i in ad.admins.values():
            if i == id:
                return True
        return False
    except:
        print("Error in user verification function")



# передает в функцию ссылку на администраторс
def set_admins_objects(administrators):
    global ad
    ad = administrators

