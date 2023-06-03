from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    main = State()
    order_id = State()
    check_info = State()
    update_status = State()
    updated_status = State()
    check_info_all = State()

    class MassSend(StatesGroup):
        message_text = State()
        add_photo = State()
        to_all_message = State()
        message_to_send = State()
        message_markup = State()
