from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def ikb_of_locations():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb1 = InlineKeyboardButton('Філіал на Салтівці', callback_data='Філіал на Салтівці')
    ikb2 = InlineKeyboardButton('Філіал на Північній Салтівці', callback_data='Філіал на Північній Салтівці')
    ikb3 = InlineKeyboardButton('Філіал у Шевченковському районі', callback_data='Філіал у Шевченковському районі')
    ikb4 = InlineKeyboardButton('Філіал у Слобідському районі', callback_data='Філіал у Слобідському районі')
    ikb5 = InlineKeyboardButton('Філіал на Холодногірському районі', callback_data='Філіал на Холодногірському районі')
    ikb6 = InlineKeyboardButton('У головне меню', callback_data='Головне меню')
    ikb.add(ikb1, ikb2, ikb3, ikb4, ikb5, ikb6)
    return ikb


def fontan_ikb():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb1 = InlineKeyboardButton('Дивитися трнсляцію', url='https://tv.ivideon.com/camera/100-EyEL0faAp2ZC1V0TGMNp2d/196608/?lang=ru')
    ikb2 = InlineKeyboardButton('Переглянути на карті', url='https://www.google.com/maps/place/Pizza.Od.Ua/@46.4496194,30.7439358,17.06z/data=!4m8!1m2!2m1!1sPizza.Od.Ua!3m4!1s0x40c633c31098fb0f:0x2975ff8b33fa10a5!8m2!3d46.449556!4d30.745567?hl=ru')
    ikb3 = InlineKeyboardButton('Назад', callback_data='Філіали 🚩')
    ikb.add(ikb1, ikb2, ikb3)
    return ikb


def sever_ikb():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb1 = InlineKeyboardButton('Дивитися трнсляцію', url='https://tv.ivideon.com/camera/100-ILKaPPKHWz33ZOKbY54xPz/131072/?lang=ru')
    ikb2 = InlineKeyboardButton('Переглянути на карті', url='https://www.google.com/maps/place/Pizza.Od.Ua🍕/@46.582517,30.8006923,17z/data=!4m8!1m2!2m1!1sPizza.Od.Ua!3m4!1s0x40c624cf7aa4caa3:0xa59b939a907742e4!8m2!3d46.5787452!4d30.790686?hl=ru')
    ikb3 = InlineKeyboardButton('Назад', callback_data='Філіали 🚩')
    ikb.add(ikb1, ikb2, ikb3)
    return ikb


def cheremuski_ikb():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb1 = InlineKeyboardButton('Дивитися трнсляцію', url='https://tv.ivideon.com/camera/100-qrRZ7IeJAuophxDtByLcan/131072/?lang=ru')
    ikb2 = InlineKeyboardButton('Переглянути на карті', url='https://www.google.com/maps/place/Pizza.Od.Ua™🍕/@46.4431284,30.7026608,16.79z/data=!4m9!1m2!2m1!1sPizza.Od.Ua!3m5!1s0x40c632527a04eb09:0x89bee622ce8b2d5b!8m2!3d46.442837!4d30.7021331!15sCgtQaXp6YS5PZC5VYSIDiAEBWg0iC3BpenphIG9kIHVhkgEWcGl6emFfZGVsaXZlcnlfc2VydmljZQ?hl=ru')
    ikb3 = InlineKeyboardButton('Назад', callback_data='Філіали 🚩')
    ikb.add(ikb1, ikb2, ikb3)
    return ikb


def centr_ikb():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb1 = InlineKeyboardButton('Дивитися трнсляцію', url='https://tv.ivideon.com/camera/100-JNTPJLmtGczQ7Rmt1HZvin/0/?lang=ru')
    ikb2 = InlineKeyboardButton('Переглянути на карті', url='https://www.google.com/maps/place/Pizza.Od.Ua™🍕/@46.4764157,30.7404266,17z/data=!4m8!1m2!2m1!1sPizza.Od.Ua!3m4!1s0x40c6319cf6cbc47d:0x4eb7d0ea709e6146!8m2!3d46.476013!4d30.7410608?hl=ru')
    ikb3 = InlineKeyboardButton('Назад', callback_data='Філіали 🚩')
    ikb.add(ikb1, ikb2, ikb3)
    return ikb


def yug_ikb():
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb1 = InlineKeyboardButton('Дивитися трнсляцію', url='https://tv.ivideon.com/camera/100-0291767e5ed51c883799d167a4583127/262144/?lang=ru')
    ikb2 = InlineKeyboardButton('Переглянути на карті', url='https://www.google.com/maps/place/Pizza.Od.Ua™🍕/@46.3907318,30.7248303,17z/data=!4m8!1m2!2m1!1sPizza.Od.Ua!3m4!1s0x40c63367b988fd1b:0x1b2c8ccedda3bbbf!8m2!3d46.3912609!4d30.726045?hl=ru')
    ikb3 = InlineKeyboardButton('Назад', callback_data='Філіали 🚩')
    ikb.add(ikb1, ikb2, ikb3)
    return ikb

