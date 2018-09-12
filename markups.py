from telebot import types

start_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
start_markup.row('/start','Помощь')

amount_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
amount_markup.row('/start')
amount_markup.row('Добавить', 'Обнулить')


