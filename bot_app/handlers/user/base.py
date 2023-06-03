import os

from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import types
from bot_app import db, markups, config
from bot_app.db.users import get_user, order_data
from bot_app.markups.Inline_keyboards.location import ikb_of_locations, fontan_ikb, sever_ikb, cheremuski_ikb, \
    centr_ikb, yug_ikb
from bot_app.markups.user.main import cancel_menu
from bot_app.states.user import User
from bot_app.misc import bot, dp


@dp.message_handler(commands='start', state='*')
async def process_start(message: Message, state: FSMContext):
    await state.finish()
    await db.users.create_user(message.from_user)
    user_data = await get_user(message.from_user.id)
    if user_data['phone_number']:
        await bot.send_message(message.from_user.id,
                               text='Вітаємо вас в чат-боті нашої бургерної!🎉',
                               reply_markup=markups.user.main.main_menu_with_phone())
        return

    await bot.send_message(message.from_user.id,
                           text='Вітаємо вас в чат-боті нашої бургерної!🎉'
                                'Для початку роботи з чат-ботом, вам необхідно поділитись номером телефону.'
                                'Ви можете натиснути на кнопку нижче👇',
                           reply_markup=markups.user.main.main_menu())


@dp.message_handler(text='Меню📋')
async def photo_of_main_menu(message: Message):
    current_dir = os.getcwd()
    photo_path = os.path.join(current_dir, 'bot_app', 'photo', 'menu.png')
    with open(photo_path, 'rb') as photo:
        await bot.send_photo(message.from_user.id, photo=photo)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contact_recieved(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text='Ваш номер додано до нашої бази',
                           reply_markup=markups.user.main.main_menu_with_phone())
    if message.contact.phone_number.startswith('+'):
        await db.users.add_phone_number(message.from_user, message.contact.phone_number[1:])
        return

    await db.users.add_phone_number(message.from_user, message.contact.phone_number)


@dp.message_handler(text='Про нас🥇')
async def about_us(message: types.Message):
    await bot.send_message(message.from_user.id,
                           text='Безкоштовна доставка гарячих і соковитих бургерів у місті Харків🍔.\n\n'
                                '🚚 До однієї години по місту.\n\n'
                                '☎️ +38063-703-54-54\n\n'
                                '⏰ 10:00-0:00')


@dp.message_handler(text='Акції🔥')
async def promotions(message: types.Message):
    current_dir = os.getcwd()
    photo_path = os.path.join(current_dir, 'bot_app', 'photo', 'promo.jpg')
    with open(photo_path, 'rb') as photo:
        await bot.send_photo(message.from_user.id, photo=photo,
                             caption='Детальніше ознайомитись з акціями можна на нашому сайті ')


@dp.message_handler(text='Написати в підтримку✍️')
async def feedback(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text='Напишіть ваше питання нижче👇 та відправте його',
                           reply_markup=cancel_menu())
    await state.set_state(User.support)


@dp.message_handler(text='Назад 🔙', state='*')
async def confirmation_order(message: Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'Головне меню',
                           reply_markup=markups.user.main.main_menu_with_phone())


@dp.message_handler(state=User.support)
async def message_to_support(message: Message, state: FSMContext):
    await bot.send_message(chat_id=config.ADMINS_ID[0], text='Звернення до підтримки')
    await bot.forward_message(chat_id=config.ADMINS_ID[0], from_chat_id=message.from_user.id,
                              message_id=message.message_id)
    await bot.send_message(message.from_user.id, text='Ваше звернення відправлене до нас', reply_markup=cancel_menu())
    await state.finish()


@dp.message_handler(text='Філіали 🚩')
async def locations_of_shops(message: Message):
    await bot.send_message(message.from_user.id, text='Перелік наших філіалів:', reply_markup=ikb_of_locations())


@dp.callback_query_handler(text='Філіали 🚩')
async def locations_of_shops(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text='Перелік наших філіалів:', reply_markup=ikb_of_locations())


@dp.callback_query_handler(text='Філіал на Салтівці')
async def fontan(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text='Філіал знаходиться за адресою:\n'
                                      '📍Зіркове містечко, вул. Армійська, 11, корпус 1, Харків \n\n'
                                      '⌛️Графік роботи філіала: \n'
                                      'Щодня. з 10:00 до 00:00',
                                 reply_markup=fontan_ikb())


@dp.callback_query_handler(text='Філіал на Північній Салтівці')
async def sever(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text='Філіал знаходиться за адресою:\n'
                                      '📍📍Кримська, 70-А, Харків \n\n'
                                      '⌛️Графік роботи філіала: \n'
                                      'Щодня з 10:00 до 22:00',
                                 reply_markup=sever_ikb())


@dp.callback_query_handler(text='Філіал у Шевченковському районі')
async def cheremuski(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text='Філіал знаходиться за адресою:\n'
                                      '📍Вулиця Радісна 2/4, Харків \n\n'
                                      '⌛️Графік роботи філіала: \n'
                                      'Щодня, з 10:00 до 00:00',
                                 reply_markup=cheremuski_ikb())


@dp.callback_query_handler(text='Філіал у Слобідському районі')
async def centr(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text='Філіал знаходиться за адресою:\n'
                                      '📍вул. Успенська, 40. Харків \n\n'
                                      '⌛️Графік роботи філіала: \n'
                                      'Щодня з 10:00 до 00:00',
                                 reply_markup=centr_ikb())


@dp.callback_query_handler(text='Філіал на Холодногірському районі')
async def yug(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text='Філіал знаходиться за адресою:\n'
                                      '📍ул. Ак. Вільямса 62 А, Харків \n\n'
                                      '⌛️Графік роботи філіала: \n'
                                      'Щодня з 10:00 до 00:00',
                                 reply_markup=yug_ikb())


@dp.message_handler(text='Замовлення 🍔')
async def order_menu(message: Message):
    await bot.send_message(message.from_user.id,
                           text='Ласкаво просимо до меню замовлень',
                           reply_markup=markups.user.main.order_menu_kb())


@dp.message_handler(text='Всі замовленя 🍟')
async def all_orders(message: Message):
    user_data = await get_user(message.from_user.id)
    orders_list = await order_data(user_data['phone_number'])
    if not orders_list:
        await bot.send_message(message.from_user.id, text='У вас ще нема замовлень')
        return

    await bot.send_message(message.from_user.id, text='Ось перелік ваших замовлень:')
    for order in orders_list:
        await bot.send_message(message.from_user.id, text='✅Замовлення номер: <b>{}</b>\n'
                                                          '📅Дата замовлення:\n<i>{}</i>\n'
                                                          '🕔Час замовлення:\n<i>{}</i>\n'
                                                          '🗒Що замовляли:\n<code>{}</code>\n'
                                                          '🚩Адреса доставки:\n<b>{}</b>'.format(order['order_number'],
                                                                                                order['date'].strftime(
                                                                                                    "%Y:%m:%d"),
                                                                                                order['date'].strftime(
                                                                                                    "%H:%M"),
                                                                                                order['products'],
                                                                                                order['address']))


@dp.message_handler(text='Замовлення в очікуванні ⏳')
async def orders_in_processing(message: Message):
    user_data = await get_user(message.from_user.id)
    orders_list = await order_data(user_data['phone_number'])
    active_orders = [order for order in orders_list if order['status'] not in ['Доставлено', 'Відмінено']]
    if active_orders:
        for order in orders_list:
            if order['status'] not in ['Доставлено', 'Відмінено']:
                await bot.send_message(message.from_user.id, text='✅Замовлення номер: <b>{}</b>\n'
                                                                  '📅Дата замовлення:\n<i>{}</i>\n'
                                                                  '🕔Час замовлення:\n<i>{}</i>\n'
                                                                  '🗒Що замовляли:\n<code>{}</code>\n'
                                                                  '🚩Адреса доставки\n{}'.format(order['order_number'],
                                                                                                order['date'].strftime(
                                                                                                    "%Y:%m:%d"),
                                                                                                order['date'].strftime(
                                                                                                    "%H:%M"),
                                                                                                order['products'],
                                                                                                order['address']))
        await bot.send_message(message.from_user.id, text='Очікуйте повідомлення про зміну статусу замовлення')
        return

    await bot.send_message(message.from_user.id, text='Немає не завершенних замовлень')


@dp.callback_query_handler(text='Головне меню')
async def main_menu_from_ikb(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await bot.send_message(call.from_user.id, text='Вітаємо вас в чат-боті pizza.od.ua!🎉')
