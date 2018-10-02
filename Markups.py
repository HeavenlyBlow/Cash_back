# -*- coding: utf-8 -*-

from telebot import types

first_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_btn = types.KeyboardButton("В главное меню")
first_markup.add(start_btn)

first_markup_main_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
manage_admins_btn = types.KeyboardButton("Администрирование")
first_markup_main_admin.add(start_btn)
first_markup_main_admin.add(manage_admins_btn)

markup_change_points = types.InlineKeyboardMarkup(row_width=2)
points_button_add = types.InlineKeyboardButton('Добавить', callback_data="add_points")
points_button_sub = types.InlineKeyboardButton('Списать', callback_data="sub_points")
points_button_back = types.InlineKeyboardButton('В главное меню', callback_data="start")
history_button = types.InlineKeyboardButton("История операций", callback_data="history")
markup_change_points.add(points_button_add, points_button_sub, history_button)

markup_change_proc = types.InlineKeyboardMarkup()
button_change_proc1 = types.InlineKeyboardButton(text="Регистрация", callback_data="reg")
button_change_proc2 = types.InlineKeyboardButton(text="Изменить процент", callback_data="change_proc")
button_change_proc3 = types.InlineKeyboardButton(text="Ввести номер", callback_data="input_number")
markup_change_proc.add(button_change_proc1, button_change_proc2)
markup_change_proc.add(button_change_proc3)

markup_start = types.InlineKeyboardMarkup()
button_start = types.InlineKeyboardButton("В главное меню", callback_data="start")
markup_start.add(button_start)

markup_in_number = types.InlineKeyboardMarkup()
button_in_number_reg = types.InlineKeyboardButton(text="Регистрация", callback_data="reg")
markup_in_number.add(button_in_number_reg)

markup_reg = types.InlineKeyboardMarkup(row_width=1)
button_reg = types.InlineKeyboardButton('Зарегистрировать', callback_data="reg")
markup_reg.add(button_reg)

markup_manage_admins = types.InlineKeyboardMarkup(row_width=2)
add_admins = types.InlineKeyboardButton(text="Добавить", callback_data="add_admin")
delete_admins = types.InlineKeyboardButton(text="Удалить", callback_data="delete_admin")
markup_manage_admins.add(add_admins, delete_admins)

markup_delete = types.ReplyKeyboardRemove()

markup_repeat_set_delete_admin = types.InlineKeyboardMarkup()
repeat_delete_button = types.InlineKeyboardButton(text="Ввести заново", callback_data="delete_admin")
markup_repeat_set_delete_admin.add(repeat_delete_button)

markup_repeat_new_admin = types.InlineKeyboardMarkup()
repeat_new_admin = types.InlineKeyboardButton(text="Ввести заново", callback_data="add_admin")
markup_repeat_new_admin.add(repeat_new_admin)

markup_back_to_info = types.InlineKeyboardMarkup()
btn_back_to_info = types.InlineKeyboardButton(text="Назад", callback_data="back_to_info")
markup_back_to_info.add(btn_back_to_info)

markup_to_info = types.InlineKeyboardMarkup()
btn_to_info = types.InlineKeyboardButton(text="К информации о номере", callback_data="to_info")
markup_to_info.add(btn_to_info)

