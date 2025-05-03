#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> order
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/3 23:21
@Desc   ：
"""
import datetime
import random
from typing import Optional
from typing import List
from pydantic import  Field, model_validator, field_validator
from app.common.utils import date as date_util
from .base import SAModelBase


class OrderItemIn(SAModelBase):

    item_id: int = Field(..., title='物品id')
    item_name: str = Field(..., title='物品名称')
    item_num: int = Field(..., title='物品数量')
    item_type: int = Field(..., title='物品类型')
    item_price: int = Field(..., title='物品单价')
    total: int = Field(..., title='物品总价')
    item_picture_url: str = Field(None, title='物品url')
    remark: Optional[str] = Field('', title='备注')

    @field_validator('item_num')
    @classmethod
    def validate_item_num(cls, v):
        if v < 0:
            raise ValueError('item_num is invalid')
        return v


class OrderIn(SAModelBase):
    order_no: str = Field(None, title='订单号')
    user_id: int = Field(..., title='用户id')
    total: int = Field(..., title='总价')
    remark: Optional[str] = Field(..., title='备注')
    extra_data: Optional[dict] = Field(None, title='额外数据')
    order_items: List[OrderItemIn] = Field(..., title='订单明细')

    @model_validator(mode='after')
    def validate_(self):
        if not self.order_no:
            self.order_no = 'O{}{}'.format(date_util.now().strftime('%Y%m%d%H%M%S'), random.randint(10000, 99999))
        return self


class OrderPayIn(SAModelBase):
    pay_no: str = Field(..., title='支付号')
    order_id: int = Field(..., title='订单号')
    money: int = Field(..., title='支付金额')
    pay_at: datetime.datetime = Field(..., title='支付时间')
    remark: Optional[str] = Field('', title='备注')
    extra_data: Optional[dict] = Field(dict(), title='额外数据')