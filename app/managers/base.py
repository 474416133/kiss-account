#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ： base
@IDE    ：PyCharm
@Author ：sven
@Date   ：2024/7/3 15:18
@Desc   ：
"""
from typing import Callable
import functools
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import update
from app.common.responses import Page
from app.models.base import Base


async def get_or_none_by_pk(model_cls: Base, pk: int, *, conn: 'Session'):
    stmt = select(model_cls).where(model_cls.id == pk)
    ret = await conn.execute(stmt)
    return ret.scalar_one_or_none()


async def get_by_pk(model_cls: Base, pk: int, *, conn: 'Session', error: Exception):
    ret = await get_or_none_by_pk(model_cls, pk, conn=conn)
    if not ret:
        raise error
    return ret


async def delete_by_pk(model_cls: Base, pk: int, *,  conn: 'Session'):
    stmt = delete(model_cls).where(model_cls.id == pk)
    ret = await conn.execute(stmt)
    return ret


def transaction(func):
    @functools.wraps(func)
    async def _wrap(*args, **kwargs):
        ret = await func(*args, **kwargs)
        await kwargs['conn'].commit()
        return ret
    return _wrap


async def paging(stmt, page=1, page_size=10, order_by=None, *, conn: 'Session', item_handler:Callable = None):
    count_stmt = select(func.count('0')).select_from(stmt)
    ret = await conn.execute(count_stmt)
    count = ret.scalar_one()
    offset = (page - 1) * page_size
    if offset >= count:
        return Page.construct([], count, page_size, page)

    filter_stmt = stmt.limit(page_size).offset(offset)
    if order_by is not None:
        filter_stmt = filter_stmt.order_by(order_by)
    ret = await conn.execute(filter_stmt)
    records = ret.scalars()
    if callable(item_handler):
        records = list(map(item_handler, records))

    return Page.construct(records, count, page_size, page)


async def  update_by_pk(model_cls: Base, pk: int, values, *, conn: 'Session'):
    stmt = update(model_cls).values(**values).filter(model_cls.id==pk)
    await conn.execute(stmt)
    await conn.commit()






