from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu():
    buttons = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = KeyboardButton('Розіслати повідомлення ✅')
    button2 = KeyboardButton('Всі невиконані замовлення ❗️')
    button3 = KeyboardButton('Всі замовлення 🗒')
    buttons.add(button1, button2, button3)
    return buttons


def cancel():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.insert(KeyboardButton('Відмінити ❌'))
    return m


def new_markup_creating():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.row(KeyboardButton('Без кнопки'))
    return m


def custom_urls_markup_dict(markup):
    m = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    for button in markup:
        m.add(InlineKeyboardButton(button['button_text'], url=button['button_url']))
    return m


def change_status():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton('Прийняте')
    m2 = KeyboardButton('Відправлене')
    m3 = KeyboardButton('Доставлено')
    m4 = KeyboardButton('Відмінено')
    m5 = KeyboardButton('Головне меню')
    m.add(m1, m2, m3, m4, m5)
    return m


def status():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    m.add(KeyboardButton('Змінити статус'), KeyboardButton('Головне меню'))
    return m
