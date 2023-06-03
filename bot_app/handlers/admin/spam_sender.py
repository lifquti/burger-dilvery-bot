import json

import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, User

from bot_app import markups, config
from bot_app.db.users import get_all
from bot_app.markups.admin.base import admin_menu
from bot_app.misc import bot, dp
from bot_app.states.admin import Admin


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Розіслати повідомлення ✅', state='*')
async def user_echo(message: Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='Перешліть в бота повідомлення для розсилки:',
                           reply_markup=markups.admin.base.cancel())
    await state.set_state(Admin.MassSend.message_to_send)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Відмінити ❌', state='*')
async def cancel(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text='Ви повернулись на адмін панель', reply_markup=admin_menu())
    await state.finish()


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.MassSend.message_to_send,
                    content_types=aiogram.types.ContentType.ANY)
async def get_message_to_send(message: Message, state: FSMContext):
    await state.update_data({'message_id': message.message_id,
                             'chat_id': message.chat.id})
    await state.set_state(Admin.MassSend.message_markup)
    await bot.send_message(message.from_user.id,
                           'Повідомлення принято, додайте кнопку до розсилки:'
                           f'Наприклад:\n\n'
                           f'ПЕРЕЙТИ НА КАНАЛ:https://t.me/+18x4WMQrtT8wZTIy',
                           reply_markup=markups.admin.base.new_markup_creating())


@dp.message_handler(text='Без кнопки', state=Admin.MassSend.message_markup)
async def skip_start_markup(message: Message, state: FSMContext):
    await state.update_data({'message_markup': json.dumps([])})
    data = await state.get_data()
    await state.finish()
    await send_post(data, message.from_user)


@dp.message_handler(state=Admin.MassSend.message_markup)
async def get_reward_message_markup(message: Message, state: FSMContext):
    if message.text.count(':') < 1:
        await bot.send_message(message.from_user.id,
                               'Не правильний формат повідомлення для кнопки!\n'
                               'Спробуйте знову!',
                               reply_markup=markups.admin.base.new_markup_creating())
        return

    try:
        await state.update_data({'message_markup': json.dumps(
            [{'button_text': button_instance.split(':')[0], 'button_url': ':'.join(button_instance.split(':')[1:])}
             for button_instance in message.text.split('\n')])})
    except Exception as e:
        await bot.send_message(message.from_user.id,
                               'Не правильний формат повідомлення для кнопки!\n'
                               'Спробуйте знову!',
                               reply_markup=markups.admin.base.new_markup_creating())
        return
    data = await state.get_data()
    await state.finish()
    await send_post(data, message.from_user)


async def send_post(data, user: User):
    user_list = await get_all()

    errors_list = []
    good = 0
    bad = 0

    await bot.send_message(user.id,
                           f"Розсилка запущена для {len(user_list)} користувачів",
                           reply_markup=markups.admin.base.admin_menu())

    markup = json.loads(data['message_markup'])

    for users in user_list:
        try:
            await bot.copy_message(users['user_id'],
                                   message_id=data['message_id'],
                                   from_chat_id=data['chat_id'],
                                   reply_markup=markups.admin.base.custom_urls_markup_dict(markup))
            good += 1
        except Exception as e:
            errors_list.append(str(e))
            bad += 1
    await bot.send_message(user.id,
                           f"Розсилка закінчена!\n" 
                           f"Доставлено: {good}\n"
                           f"Не доставлено: {bad}\n\n"
                           f"Список помилок: {set(errors_list)}")
