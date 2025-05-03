#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> order
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/3 22:21
@Desc   ：
"""
import datetime
import enum
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import BOOLEAN
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import SMALLINT
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.models.base import fk
from app.models.base import Base
from app.models.base import RecordMixin



class Order(RecordMixin, Base):
    __tablename__ =  'order'
    order_no: Mapped[str] = mapped_column(String(100), comment='订单号')
    user_id: Mapped[fk] = mapped_column(ForeignKey("user_account.id"), comment='用户id')
    total: Mapped[int] = mapped_column(INTEGER, comment='总价')
    payed_money: Mapped[int] = mapped_column(INTEGER, default=0, comment='已支付金额')
    remark: Mapped[Optional[str]] = mapped_column(String(100), default='', comment='备注')
    inbounded: Mapped[bool] = mapped_column(BOOLEAN, default=False, comment='是否入库')
    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict(), comment='其他信息')

    @property
    def finished(self):
        return self.payed_money == self.total


class OrderItem(RecordMixin, Base):
    __tablename__ = 'order_item'
    order_id: Mapped[fk] = mapped_column(ForeignKey("order.id"), comment='订单号')
    item_id: Mapped[fk] = mapped_column(ForeignKey("item.id"), comment='物品id')
    item_name: Mapped[str] = mapped_column(String(100), comment='物品名称')
    item_num: Mapped[int] = mapped_column(INTEGER, default=1, comment='数量')
    item_price: Mapped[int] = mapped_column(INTEGER, comment='单价')
    item_type: Mapped[int] = mapped_column(SMALLINT, comment='物品类型')
    item_picture_url: Mapped[str] = mapped_column(String(300), comment='物品名称')
    total: Mapped[int] = mapped_column(INTEGER, comment='总价')
    remark: Mapped[Optional[str]] = mapped_column(String(100), default=None, comment='备注')
    is_used: Mapped[bool] = mapped_column(BOOLEAN, default=False, comment='是否已使用')

    order: Mapped['Order'] = relationship()


class OrderPay(RecordMixin, Base):
    __tablename__ = 'order_pay'
    pay_no: Mapped[str] = mapped_column(String(100), comment='支付单号')
    order_id: Mapped[fk] = mapped_column(ForeignKey("order.id"), comment='订单号')
    money: Mapped[int] = mapped_column(INTEGER, default=1, comment='已支付')
    pay_at: Mapped[datetime.datetime]  = mapped_column(TIMESTAMP, comment='支付时间')
    remark: Mapped[Optional[str]] = mapped_column(String(100), default='', comment='备注')
    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB, default=dict(), comment='其他信息')



