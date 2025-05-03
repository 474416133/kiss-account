#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> item
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/3 22:34
@Desc   ：
"""
from typing import List
from sqlalchemy import select, or_
from sqlalchemy import update
from app.common.utils import date
from app.predefine import errors
from app.models.item import Item
from app.models.item import SubItem
from app.schemas.item import ItemIn
from app.managers.base import paging


async def create_item(item: ItemIn, *,  conn: 'Session'):
    item_obj = item.to_orm(Item, exclude=['items'])
    items = [item_obj]
    for sub_item in item.items:
        sub_item_obj = sub_item.to_orm(SubItem)
        sub_item_obj.parent = item_obj
        items.append(sub_item_obj)

    conn.add_all(items)
    await conn.commit()


async def page_item(conditions: dict, page: int =1, page_size: int =10, order_by=None,  *, conn: 'Session' ):
    stmt = select(Item)
    keyword = conditions.pop('keyword', None)
    if keyword:
        stmt = stmt.filter(or_(Item.name.contains(keyword), Item.tags.any([keyword])))
    if conditions:
        stmt = stmt.filter_by(**conditions)
    return await paging(stmt, page, page_size, order_by, conn=conn)



