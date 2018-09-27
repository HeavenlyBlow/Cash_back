# -*- coding: utf-8 -*-
import Vars


ad = ''


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def check_user(id):
    try:
        for j in ad.main_admins.values():
            if j == id:
                Vars.accept_user = get_key(ad.main_admins, j)
                Vars.admin_is_main = True
                return True
        for i in ad.admins.values():
            if i == id:
                Vars.accept_user = get_key(ad.admins, i)
                return True
    except:
        print("Error in user verification function")
    return False

# передает в функцию ссылку на администраторс
def set_admins_objects(administrators):
    global ad
    ad = administrators

