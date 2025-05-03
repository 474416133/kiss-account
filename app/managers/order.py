#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> order
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/3 23:20
@Desc   ：
"""
import logging
from typing import List
from typing import Optional
from sqlalchemy import update
from sqlalchemy import select
from app.predefine import errors
from app.models.order import Order
from app.models.order import OrderItem
from app.models.order import OrderPay
from app.schemas.order import OrderIn
from app.schemas.order import OrderPayIn
from app.managers.base import get_by_pk, paging


logger = logging.getLogger('kiss-account')


async def create_order(order: OrderIn, *, conn):
    order_obj = order.to_orm(Order, exclude=['order_items'])
    order_obj.order_items = []
    for order_item in order.order_items:
        order_item_obj = order_item.to_orm(OrderItem)
        order_item_obj.order = order_obj
        order_obj.order_items.append(order_item_obj)

    conn.add_all([order_obj] + order_obj.order_items)
    await conn.commit()
    return  order_obj


async def get_order_items(order_id: int, *, conn: 'Session') -> List[Optional[OrderItem]]:

    stmt = select(OrderItem).where(OrderItem.order_id==order_id)
    ret = await conn.execute(stmt)
    return ret.scalars()


async def create_order_pay(order_pay: OrderPayIn, *, conn: 'Session'):
    order = await get_by_pk(Order,
                      order_pay.order_id,
                      error=errors.DATA_NOT_EXIST('order is unavailable'),
                      conn=conn)
    rest_money = order.total - order.payed_money

    if rest_money < order_pay.money:
        raise errors.ORDER_MONEY_ERROR('pay fail: money payed is overflow')

    pay_obj = order_pay.to_orm(OrderPay)
    conn.add(pay_obj)
    update_stmt = update(Order).values(payed_money = Order.payed_money + pay_obj.money).where(Order.id == pay_obj.order_id)
    await conn.execute(update_stmt)
    await conn.commit()


async def page_user_item(conditions: dict, page: int =1, page_size: int =10, order_by=None,  *, conn: 'Session' ):
    stmt = select(OrderItem).join(Order, Order.id == OrderItem.order_id)
    keyword = conditions.pop('keyword', None)
    if keyword:
        stmt = stmt.filter(OrderItem.name.contains(keyword))
    user_id = conditions.pop('user_id', None)
    if user_id:
        stmt = stmt.filter(Order.user_id == user_id)
    if conditions:
        stmt = stmt.filter_by(**conditions)
    return await paging(stmt, page, page_size, order_by, conn=conn)