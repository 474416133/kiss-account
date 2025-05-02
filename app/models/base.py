#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ： base
@IDE    ：PyCharm
@Author ：sven
@Date   ：2022/2/26 17:55
@Desc   ：
"""
import logging
import datetime
from typing_extensions import Annotated
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import BIGINT

from app.common.utils import date


logger = logging.getLogger('kiss-account.models')
pk = Annotated[int, mapped_column(BIGINT, primary_key=True)]
fk = Annotated[int, mapped_column(BIGINT)]


def get_column_names(model_cls):
    """

    :param model_cls:
    :return:
    """
    return (c.name for c in class_mapper(model_cls).c)


class Base(DeclarativeBase): pass


class RecordMixin:
    """
    记录
    """
    # __abstract__ = True
    id: Mapped[pk]  = mapped_column(autoincrement=True, comment='id')
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, default=date.now,
                                                          comment='创建时间')
    modified_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False, default=date.now,
                                                          comment='最近更新时间')

    @classmethod
    def from_schema(cls, model, *args, **kwargs):
        instance = cls(**model.dict(*args, **kwargs))
        now = date.now()
        instance.created_at = now
        instance.modified_at = now
        return instance


class Choice(object):
    """
    enum.Enum
    """
    @classmethod
    def choices(cls):
        """
        :return:
        """
        return [(member.value, name) for name, member in cls.__members__.items()]

