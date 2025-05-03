#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> user
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/3 22:40
@Desc   ：
"""
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from app.schemas.base import SAModelBase, PasswordType



class UserRegister(SAModelBase):
    username: str = Field(..., description='用户名')
    password: str = Field(..., description='密码')
    password_confirmed: str = Field(..., description='确认的密码')
    nickname: Optional[str] = Field(None, description='昵称')
    avatar_url: str = Field(None, description='头像链接')

    @model_validator(mode='after')
    def validate_(self):
        if self.password_confirmed != self.password:
            raise ValueError('password != password_confirmed')
        if not self.nickname:
            self.nickname = self.username
        return self



class UserPassword(BaseModel):
    password_type0: PasswordType = Field(default=PasswordType.PASSWORD, description='密码模式登录类型')
    code_or_password0: str = Field(..., description='原始密码')
    password: str = Field(..., description='密码')
    password_confirmed: str = Field(..., description='确认的密码')

    @model_validator(mode='after')
    def validate_(self):
        if self.password_type0 == PasswordType.PASSWORD and self.password == self.code_or_password0:
            raise ValueError('新密码和旧密码不能一样')

        if self.password_confirmed != self.password:
            raise ValueError('password != password_confirmed')
        return self
