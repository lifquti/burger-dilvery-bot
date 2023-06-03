from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    phone_number = State()
    create_order = State()
    address = State()
    confirmation = State()
    comment = State()
    support = State()
