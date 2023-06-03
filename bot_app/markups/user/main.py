from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton('Поділитись номером📱', request_contact=True)
    m2 = KeyboardButton('Написати в підтримку✍️')
    m3 = KeyboardButton('Акції🔥')
    m4 = KeyboardButton('Про нас🥇')
    m5 = KeyboardButton('Філіали🍽')
    m.add(m1).add(m2, m3, m4, m5)
    return m


def main_menu_with_phone():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton('Меню📋')
    m2 = KeyboardButton('Замовлення 🍔')
    m3 = KeyboardButton('Написати в підтримку✍️')
    m4 = KeyboardButton('Акції🔥')
    m5 = KeyboardButton('Про нас🥇')
    m6 = KeyboardButton('Філіали 🚩')
    m.add(m1).add(m2).add(m3, m4, m5, m6)
    return m


def cancel():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.insert(KeyboardButton('Відмінити❌'))
    return m


def cancel_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.insert(KeyboardButton('Назад 🔙'))
    return m


def yes_or_no():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton('Так ✅')
    m2 = KeyboardButton('Ні ❌')
    m.add(m1, m2)
    return m


def comment_keyboard():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    m1 = KeyboardButton('Без коментаря')
    m2 = KeyboardButton('Головне меню')
    m.add(m1, m2)
    return m


def order_menu_kb():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton('Всі замовленя 🍟')
    m2 = KeyboardButton('Замовлення в очікуванні ⏳')
    m3 = KeyboardButton('Зробити замовлення 📝')
    m4 = KeyboardButton('Назад 🔙')
    m.add(m1, m2, m3, m4)
    return m
