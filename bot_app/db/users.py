import datetime

from aiogram.types import User

from bot_app.db.base import create_dict_con


async def create_user(user: User):
    con, cur = await create_dict_con()
    await cur.execute('insert ignore into data_tg_user (user_id, name, user_name)'
                      'values (%s, %s, %s)',
                      (user.id, user.first_name, user.username))
    await con.commit()
    await con.ensure_closed()


async def add_phone_number(user: User, contact):
    con, cur = await create_dict_con()
    await cur.execute('update data_tg_user set phone_number = %s where user_id = %s', (contact, user.id))
    await con.commit()
    await con.ensure_closed()


async def get_user(user_id):
    con, cur = await create_dict_con()
    await cur.execute('select * from data_tg_user where user_id = %s', (user_id,))
    user_data = await cur.fetchone()
    await con.ensure_closed()
    return user_data


async def get_latest_order():
    con, cur = await create_dict_con()
    await cur.execute('select * from orders order by order_number desc limit 1')
    order_info = await cur.fetchone()
    await con.ensure_closed()
    return order_info


async def order_data(phone):
    con, cur = await create_dict_con()
    await cur.execute('select * from orders where phone_number = %s', (phone,))
    orders_data = await cur.fetchall()
    await con.ensure_closed()
    return orders_data


async def get_all():
    con, cur = await create_dict_con()
    await cur.execute('select * from data_tg_user')
    users = await cur.fetchall()
    await con.ensure_closed()
    return users


async def create_order(info: dict, phone: int):
    con, cur = await create_dict_con()
    await cur.execute('insert ignore into orders (phone_number, address, products, comment, status, date)'
                      'values (%s, %s, %s, %s, %s, %s)',
                      (phone, info['address'], info['order_text'], info['comment'], 'Нове', datetime.datetime.now()))
    await con.commit()
    await con.ensure_closed()


async def get_status_order(order_id: int):
    con, cur = await create_dict_con()
    await cur.execute('select status from orders where order_number = %s', (order_id, ))
    order_info = await cur.fetchone()
    await con.ensure_closed()
    return order_info


async def change_order_status_in_table(change):
    con, cur = await create_dict_con()
    await cur.execute('update orders set status = %s where order_number = %s', (change['changed_status'], change['order_id']))
    await con.commit()
    await con.ensure_closed()


async def user_phone_for_change_status(change):
    con, cur = await create_dict_con()
    await cur.execute('select phone_number from orders where order_number = %s', (change['order_id']))
    user_phone_number = await cur.fetchone()
    await con.ensure_closed()
    return user_phone_number


async def get_user_by_phone(num):
    con, cur = await create_dict_con()
    await cur.execute('select user_id from data_tg_user where phone_number = %s', (num, ))
    user_id_from_data = await cur.fetchone()
    await con.ensure_closed()
    return user_id_from_data


async def get_all_orders():
    con, cur = await create_dict_con()
    await cur.execute('select * from orders')
    dict_all_orders = await cur.fetchall()
    await con.ensure_closed()
    return dict_all_orders


async def get_info_by_order_number(order_id):
    con, cur = await create_dict_con()
    await cur.execute('select * from orders where order_number = %s', (order_id,))
    dict_orders_info = await cur.fetchone()
    await con.ensure_closed()
    return dict_orders_info
