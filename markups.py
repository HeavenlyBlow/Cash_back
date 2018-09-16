from telebot import types

start_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
start_markup.row('Помощь')

markup_change_points = types.InlineKeyboardMarkup(row_width=2)
points_button_add = types.InlineKeyboardButton('Добавить',callback_data="add_points")
points_button_sub = types.InlineKeyboardButton('Обнулить',callback_data="sub_points")
markup_change_points.add(points_button_add,points_button_sub)

markup_change_proc = types.InlineKeyboardMarkup()
button_change_proc = types.InlineKeyboardButton(text="Изменить процент", callback_data="change_proc")

markup_change_proc.add(button_change_proc)

markup_start = types.InlineKeyboardMarkup()
button_start = types.InlineKeyboardButton("В главное меню", callback_data="start")
markup_start.add(button_start)



