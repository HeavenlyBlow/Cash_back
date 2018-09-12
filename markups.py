from telebot import types

start_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
start_markup.row('/start')
start_markup.row('Установка процента', 'Помощь')

amount_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
amount_markup.row('/start')
amount_markup.row('Добавить', 'Обнулить')


