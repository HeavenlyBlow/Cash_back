import database as db
import vars
def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def check_user(id):
    try:
        for i in db.admins.values():
            if i == id:
                vars.accept_user = get_key(db.admins, i)
                return True

        for j in db.main_admins.values():
            if j == id:
                vars.accept_user = get_key(db.main_admins, j)
                vars.admin_is_main = True
                return True
    except:
        print("Ошибка в функции проверки юзера")
    return False