#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> schemas
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/2 20:40
@Desc   ：
"""
import enum
from typing import Optional
import string
from pydantic import BaseModel, Field, model_validator, ConfigDict
from pydantic import field_validator
from app.predefine import AuthorizeFail


@enum.unique
class PasswordType(enum.IntEnum):
    PASSWORD = 1
    EMAIL_CODE = 2
    MOBILE_CODE = 4


class PasswordMode(BaseModel):
    password_type: PasswordType = Field(default=PasswordType.PASSWORD, description='密码模式登录类型')
    username: str = Field(..., description='密码模式登录类型')
    password: str = Field(..., description='密码/code')


class PasswordCode(BaseModel):
    password_type: PasswordType = Field(default=PasswordType.EMAIL_CODE, description='密码模式登录类型')
    username: str = Field(..., description='email/mobile')

    @model_validator(mode='after')
    def validate_(self):
        if self.password_type == PasswordType.PASSWORD:
            raise ValueError('password_type参数错误')
        return self



class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description='id')
    nickname: str = Field(..., description='昵称')
    avatar_url: str = Field(..., description='头像url')



class AccessToken(BaseModel):
    token: str = Field(..., description='token')
    expired_at: int = Field(..., description='超时时间点')
    # refresh_token: str = Field(..., description='刷新token')
    token_type: str = Field(default='Bear', description='token类型')
    user: User = Field(..., description='用户信息')



class SAModelBase(BaseModel):

    def to_orm(self, orm_cls, **kwargs):
        return orm_cls(**self.dict(**kwargs))


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


class Client(BaseModel):
    client_id: int| str = Field(default=0, description='客户端id')
    client_ip: str | None = Field(default=None, description='客户端ip')

    @model_validator(mode='after')
    def validate_(self):
        if isinstance(self.client_id, str):
            if not self.client_id.isdigit():
                raise AuthorizeFail('client_id不合法')
            try:
                self.client_id = int(self.client_id)
            except:
                raise AuthorizeFail('client_id不合法')

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
