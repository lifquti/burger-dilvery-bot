import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_app import config
from bot_app.misc import dp
from bot_app.misc import bot, dp





@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state='*')
async def process_start(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'pls press /admin')


@dp.message_handler(state='*')
async def process_start(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'pls press /start')

