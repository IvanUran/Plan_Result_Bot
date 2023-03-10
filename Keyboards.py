"""
Файл со всеми аиограм клавитурами.
"""
from aiogram import types

choose_fighter_reply = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = types.reply_keyboard.KeyboardButton('ПЛАН')
# button_2 = types.reply_keyboard.KeyboardButton('ИТОГ(не нажимай на меня)')
button_3 = types.reply_keyboard.KeyboardButton('Мои показатели')
# choose_fighter_reply.row(button_1, button_2)
choose_fighter_reply.row(button_1)
choose_fighter_reply.row(button_3)


button_feelings = types.InlineKeyboardButton('Как себя чувствуешь?', callback_data='feelings')
button_motivation = types.InlineKeyboardButton('Какая мотивация(от 1 до 100)?', callback_data='motivation')
button_sleep = types.InlineKeyboardButton('Сколько спал?', callback_data='sleep')
button_do = types.InlineKeyboardButton('Что хочешь сделать?', callback_data='do')
button_complete = types.InlineKeyboardButton('План завершён', callback_data='complete')

plan_inline1 = types.InlineKeyboardMarkup()
plan_inline2 = types.InlineKeyboardMarkup()
plan_inline3 = types.InlineKeyboardMarkup()
plan_inline4 = types.InlineKeyboardMarkup()
plan_inline1.row(button_feelings)
plan_inline2.row(button_motivation)
plan_inline3.row(button_sleep)
plan_inline4.row(button_complete)

yes_no_inline = types.InlineKeyboardMarkup()
button_yes = types.InlineKeyboardButton('Да', callback_data='yes')
button_no = types.InlineKeyboardButton('Нет', callback_data='no')
button_del = types.InlineKeyboardButton('Удалить план', callback_data='del')
yes_no_inline.row(button_yes, button_no)
yes_no_inline.row(button_del)
