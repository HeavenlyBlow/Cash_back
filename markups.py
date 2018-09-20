from telebot import types
first_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_btn = types.KeyboardButton("В главное меню")
first_markup.add(start_btn)





markup_change_points = types.InlineKeyboardMarkup(row_width=2)
points_button_add = types.InlineKeyboardButton('Добавить',callback_data="add_points")
points_button_sub = types.InlineKeyboardButton('Списать',callback_data="sub_points")
points_button_back = types.InlineKeyboardButton('В главное меню', callback_data="start")
history_button = types.InlineKeyboardButton("Последние 10 операций", callback_data="history")
markup_change_points.add(points_button_add,points_button_sub,history_button)

markup_change_proc = types.InlineKeyboardMarkup()
button_change_proc1 = types.InlineKeyboardButton(text="Регистрация", callback_data="reg")
button_change_proc2 = types.InlineKeyboardButton(text="Изменить процент", callback_data="change_proc")
button_change_proc3 = types.InlineKeyboardButton(text="Ввести номер", callback_data="input_number")
markup_change_proc.add(button_change_proc1,button_change_proc2)
markup_change_proc.add(button_change_proc3)


markup_start = types.InlineKeyboardMarkup()
button_start = types.InlineKeyboardButton("В главное меню", callback_data="start")
markup_start.add(button_start)

markup_in_number = types.InlineKeyboardMarkup()
button_in_number_reg = types.InlineKeyboardButton(text="Регистрация", callback_data="reg")
button_in_number_back = types.InlineKeyboardButton(text="Главное меню", callback_data="start")
markup_in_number.add(button_in_number_reg)

markup_reg = types.InlineKeyboardMarkup(row_width=1)
button_reg = types.InlineKeyboardButton('Зарегистрировать',callback_data="reg")
markup_reg.add(button_reg)


