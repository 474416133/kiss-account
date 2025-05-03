#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> user
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/2 15:14
@Desc   ：
"""
import datetime
import enum
from typing import Optional
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import SMALLINT
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.dialects.postgresql import BOOLEAN
from sqlalchemy.dialects.postgresql import CHAR
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from app.models.base import fk
from app.models.base import Base
from app.models.base import RecordMixin
from app.models.base import Choice


@enum.unique
class AccountState(Choice, enum.IntEnum):
    INACTIVE = 0
    ACTIVE = 1
    FREEZE = 2


AccountStateChoice = AccountState.choices()


class User(RecordMixin, Base):
    __tablename__ = 'user_account'
    username: Mapped[str] = mapped_column(String(64), unique=True, comment='用户名')
    password_encrypted: Mapped[Optional[str]] = mapped_column(TEXT, comment='加密密码')
    nickname: Mapped[str] = mapped_column(String(30), comment='昵称')
    avatar_url: Mapped[str] = mapped_column(String(300), comment='头像url')
    enabled: Mapped[bool] = mapped_column(BOOLEAN, default=True, comment='是否可用')
    enabled_remark: Mapped[Optional[str]] = mapped_column(String(60), comment='备注')
    last_login_ip: Mapped[Optional[str]] = mapped_column(String(50), comment='最后登录时间')



class UserEmail(RecordMixin, Base):
    __tablename__ = 'user_email'

    username: Mapped[str]  = mapped_column(String(64), unique=True, comment='用户名')
    activated: Mapped[bool]  = mapped_column(BOOLEAN, default=False, comment='是否激活')
    activate_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, comment='激活时间')
    user_id: Mapped[fk]  = mapped_column(ForeignKey("user_account.id"))
    activate_ip: Mapped[Optional[str]] = mapped_column(TEXT, comment='激活ip')

    user: Mapped['User'] = relationship()



class UserMobile(RecordMixin, Base):
    __tablename__ = 'user_mobile'

    username: Mapped[str]  = mapped_column(String(30), unique=True, comment='用户名')
    activated: Mapped[bool]  = mapped_column(BOOLEAN, default=False, comment='是否激活')
    activate_at: Mapped[Optional[datetime.datetime]]  = mapped_column(TIMESTAMP, comment='激活时间')
    user_id: Mapped[fk] = mapped_column(ForeignKey("user_account.id"))
    activate_ip: Mapped[Optional[str]] = mapped_column(TEXT, comment='激活ip')
    user: Mapped['User'] = relationship()



class UserPasswordCode(RecordMixin, Base):
    __tablename__ = 'user_password_code'

    user_id: Mapped[Optional[fk]] = mapped_column(ForeignKey("user_account.id"))
    username: Mapped[str] = mapped_column(String(64), comment='用户名')
    code: Mapped[str] = mapped_column(String(6), comment='登录用的code')
    expired_at: Mapped[int] = mapped_column(BIGINT)
    client_id: Mapped[fk] = mapped_column(comment='client_id')
    client_ip: Mapped[Optional[str]] = mapped_column(TEXT, default='', comment='激活ip')
    user: Mapped['User'] = relationship()


