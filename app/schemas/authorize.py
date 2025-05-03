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
from pydantic import BaseModel, Field, model_validator, ConfigDict
from app.predefine import AuthorizeFail
from app.schemas.base import SAModelBase, PasswordType



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


