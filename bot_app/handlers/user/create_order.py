from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from bot_app import db, markups, states, config
from bot_app.db.users import get_user, get_latest_order
from bot_app.markups.user.main import main_menu_with_phone
from bot_app.states.user import User

from bot_app.misc import bot, dp


@dp.message_handler(text='Зробити замовлення 📝')
async def create_order(message: Message, state: FSMContext):
    user_data = await get_user(message.from_user.id)
    if user_data['phone_number']:
        await bot.send_message(message.from_user.id,
                               text='Напишіть нижче що ви хочете замовити:\n\n',
                               reply_markup=markups.user.main.cancel())
        await state.set_state(User.create_order)
        return

    await bot.send_message(message.from_user.id,
                           text='Вітаємо вас в чат-боті pizza.od.ua!🎉'
                                'Для початку роботи з чат-ботом, вам необхідно поділитись номером телефону.'
                                'Ви можете натиснути на кнопку нижче👇',
                           reply_markup=markups.user.main.main_menu())


@dp.message_handler(text='Відмінити❌', state='*')
async def cancel(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text='Ви повернулись на головне меню',
                           reply_markup=main_menu_with_phone())
    await state.finish()


@dp.message_handler(state=states.user.User.create_order)
async def confirmation_order(message: Message, state: FSMContext):
    await state.update_data({'order_text': message.text,
                             'chat_id': message.chat.id})
    await bot.send_message(message.from_user.id, 'Будь ласка напишіть адресу доставки',
                           reply_markup=markups.user.main.cancel_menu())
    await state.set_state(User.address)


@dp.message_handler(state=User.address)
async def comment(message: Message, state: FSMContext):
    await state.update_data({'address': message.text})
    await bot.send_message(message.from_user.id, 'Напишить коментар до замовлення',
                           reply_markup=markups.user.main.comment_keyboard())
    await state.set_state(User.comment)


@dp.message_handler(text='Без коментаря', state=User.comment)
async def add_addres_without_comment(message: Message, state: FSMContext):
    await state.update_data({'comment': ''})

    order_details = await state.get_data()
    await bot.send_message(message.from_user.id, 'Підтверджуєте замовлення?\n{}'
                                                 '\nЗа адресою\n{} '
                                                 '\nБез коментаря\n'.format(order_details['order_text'],
                                                                            order_details['address']),
                           reply_markup=markups.user.main.yes_or_no())
    await state.set_state(User.confirmation)


@dp.message_handler(state=User.comment)
async def add_address(message: Message, state: FSMContext):
    await state.update_data({'comment': message.text})
    order_details = await state.get_data()
    await bot.send_message(message.from_user.id, 'Підтверджуєте замовлення?\n{}'
                                                 '\nЗа адресою\n{} '
                                                 '\nКоментар\n{}'.format(order_details['order_text'],
                                                                         order_details['address'],
                                                                         order_details['comment']),
                           reply_markup=markups.user.main.yes_or_no())
    await state.set_state(User.confirmation)


@dp.message_handler(text='Ні ❌', state=User.confirmation)
async def negative_confirmation(message: Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'Головоне меню',
                           reply_markup=markups.user.main.main_menu_with_phone())


@dp.message_handler(text='Так ✅', state=User.confirmation)
async def positive_confirmation(message: Message, state: FSMContext):
    order_info = await state.get_data()
    user_data = await get_user(message.from_user.id)
    await db.users.create_order(order_info, user_data['phone_number'])
    latest_order = await get_latest_order()
    await bot.send_message(chat_id=config.ADMINS_ID[0], text='✅Нове замовлення:\n'
                                                             '📞Номер замовлення\n\t{}\n'
                                                             'Номер телефона замовника\n\t{}\n'
                                                             '🗒Перелік замовлення\n\t{}\n'
                                                             '🚩Aдреса доставки\n\t{}\n'
                                                             '🕑Час замовлення\n\t{}\n'
                                                             '📝Коментар\n\t{}'.format(latest_order['order_number'],
                                                                                     latest_order['phone_number'],
                                                                                     latest_order['products'],
                                                                                     latest_order['address'],
                                                                                     latest_order['date'].strftime("%m/%d/%Y, %H:%M"),
                                                                                     latest_order['comment']))
    await bot.send_message(message.from_user.id, text='Ваше замовлення прийняте',
                           reply_markup=markups.user.main.main_menu_with_phone())
    await state.finish()


@dp.message_handler(state=User.confirmation)
async def negative_confirmation(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Виберіть так або ні',
                           reply_markup=markups.user.main.yes_or_no())
