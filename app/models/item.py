#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> item
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/3 22:22
@Desc   ：
"""
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.dialects.postgresql import BOOLEAN
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.models.base import fk
from app.models.base import Base
from app.models.base import RecordMixin


class Item(RecordMixin, Base):

    __tablename__ = 'item'

    name: Mapped[str] = mapped_column(String(100), unique=True, comment='name pot')
    price: Mapped[int] = mapped_column(INTEGER, default=0, comment='价格')
    picture_url: Mapped[str] = mapped_column(String(300), comment='商品图片链接')
    tags: Mapped[list] = mapped_column(ARRAY(TEXT), comment='标签')
    on_sale: Mapped[bool] = mapped_column(BOOLEAN, comment='是否上架')
    remark: Mapped[str] = mapped_column(String(100), comment='备注')
    is_deleted: Mapped[bool] = mapped_column(BOOLEAN, default=False, comment='其他额外数据')
    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB, comment='其他额外数据')



class SubItem(RecordMixin, Base):

    __tablename__ = 'sub_item'
    parent_id: Mapped[fk] = mapped_column(ForeignKey("item.id"), comment='物品id')
    item_id: Mapped[fk] = mapped_column(ForeignKey("item.id"), comment='物品id')
    item_num: Mapped[int] = mapped_column(INTEGER, comment='物品id')

    parent: Mapped['Item'] = relationship()