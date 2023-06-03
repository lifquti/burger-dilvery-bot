import datetime

import aiogram

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from bot_app import markups, config
from bot_app.db.users import change_order_status_in_table, user_phone_for_change_status, \
    get_user_by_phone, get_all_orders, get_info_by_order_number
from bot_app.markups.admin.base import cancel, change_status, status
from bot_app.misc import bot, dp
from bot_app.states.admin import Admin


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), commands=['admin'], state='*')
async def process_start(message: Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id,
                           'Вітаю у адмін панелі',
                           reply_markup=markups.admin.base.admin_menu())


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Головне меню', state='*')
async def process_start(message: Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id,
                           'Головне меню',
                           reply_markup=markups.admin.base.admin_menu())
    await state.finish()


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Всі невиконані замовлення ❗️')
async def all_orders(message: Message, state: FSMContext):
    dict_of_all_orders = await get_all_orders()
    list_of_orders = [
        ', '.join(str(value) for key, value in one_order.items() if key not in ['products', 'comment', 'address']) for
        one_order in dict_of_all_orders if one_order['status'] in ['Нове', 'Прийняте', 'Відправлене']]
    new_list = []
    for order in list_of_orders:
        order = '/' + order
        new_list.append(order)
    orders_text = '\n\n'.join(new_list)
    await state.set_state(Admin.check_info)
    if orders_text:
        await bot.send_message(message.from_user.id,
                               text='Всі активні заявки:\n\n{}\n\n Натисніть на номер ордеру щоб побачити дельнішу '
                                    'інформацію та змінити статус'.format(orders_text), reply_markup=cancel())
        return

    await bot.send_message(message.from_user.id, text='Немає активних заявок', reply_markup=cancel())


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), regexp=r'^\/+', state=Admin.check_info)
async def check_order(message: Message, state: FSMContext):
    order_info = await get_info_by_order_number(message.text[1:])
    await bot.send_message(message.from_user.id, text=f'Номер заявки:\n{order_info["order_number"]}\n'
                                                      f'📞Телефоний номер замовника:\n{order_info["phone_number"]}\n'
                                                      f'🚩Адреса доставки:\n{order_info["address"]}\n'
                                                      f'🗒Замовлення:\n{order_info["products"]}\n'
                                                      f'📝Коментар до замовлення:\n{order_info["comment"]}\n'
                                                      f'Статус:\n{order_info["status"]}\n'
                                                      f'🕑Дата створення:\n{order_info["date"]}\n',
                           reply_markup=status())
    await state.update_data({'order_id': message.text[1:]})
    await state.set_state(Admin.update_status)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.update_status)
async def order_id(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Виберіть на що змінити', reply_markup=change_status())
    await state.set_state(Admin.updated_status)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.updated_status)
async def status_order(message: Message, state: FSMContext):
    await state.update_data({'changed_status': message.text})
    order_for_change = await state.get_data('order_id')
    await change_order_status_in_table(order_for_change)

    await bot.send_message(message.from_user.id,
                           text='Замовлення номер:\n<b>{}</b>\n ❗️Новий статус:\n<b>{}</b>'.format(
                               order_for_change['order_id'],
                               order_for_change[
                                   'changed_status']))
    user_phone = await user_phone_for_change_status(order_for_change)
    user_id_for_change = await get_user_by_phone(user_phone['phone_number'])
    await bot.send_message(chat_id=user_id_for_change['user_id'],
                           text='❗️Оновлено статус замовлення❗️\n\t<b>{}</b>'.format(
                               order_for_change['changed_status']))
    await bot.send_message(message.from_user.id, text='Головне меню', reply_markup=markups.admin.base.admin_menu())
    await state.finish()


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Всі замовлення 🗒')
async def all_orders(message: Message, state: FSMContext):
    dict_of_all_orders = await get_all_orders()
    list_of_orders = [
        ', '.join(
            str(value) for key, value in one_order.items() if key not in ['products', 'comment', 'address', 'status'])
        for
        one_order in dict_of_all_orders]
    new_list = []
    for order in list_of_orders:
        order = '/' + order
        new_list.append(order)
    orders_text = '\n\n'.join(new_list)
    if orders_text:
        await bot.send_message(message.from_user.id, text='Всі замовлення:\n\n{}'.format(orders_text),
                               reply_markup=cancel())
    await state.set_state(Admin.check_info_all)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), regexp=r'^\/+', state=Admin.check_info_all)
async def info_one_order(message: Message, state: FSMContext):
    order_info = await get_info_by_order_number(message.text[1:])
    await bot.send_message(message.from_user.id, text=f'✅Номер заявки:\n<b>{order_info["order_number"]}</b>\n'
                                                      f'📞Телефоний номер замовника:\n{order_info["phone_number"]}\n'
                                                      f'🚩Адреса доставки:\n<b>{order_info["address"]}</b>\n'
                                                      f'🗒Замовлення:\n<code>{order_info["products"]}</code>\n'
                                                      f'📝Коментар до замовлення:\n<code>{order_info["comment"]}</code>\n'
                                                      f'Статус:\n{order_info["status"]}\n'
                                                      f'🕑Дата створення:\n<i>{order_info["date"]}</i>\n',
                           reply_markup=cancel())
    await state.finish()
