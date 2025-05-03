#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> base
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/3 22:40
@Desc   ：
"""
import enum
from pydantic import BaseModel


class SAModelBase(BaseModel):

    def to_orm(self, orm_cls, **kwargs):
        return orm_cls(**self.dict(**kwargs))


@enum.unique
class PasswordType(enum.IntEnum):
    PASSWORD = 1
    EMAIL_CODE = 2
    MOBILE_CODE = 4

