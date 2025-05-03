#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> __init__.py
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/3 1:17
@Desc   ：
"""
from fastapi import APIRouter
from fastapi import Query
from fastapi import Body
from app.common.responses import Response
from app.common.responses import OK
from app.managers import user as user_mgr
from app.routers.schemas import AccessToken
from app.routers.schemas import PasswordMode
from app.routers.schemas import PasswordCode

from app.routers.depends import Conn
from app.routers.depends import Client

router = APIRouter(prefix='/oauth2')


@router.post('/token',
             summary='获取token',
             response_model=Response[AccessToken])
async def get_token(client: Client,
                    conn: Conn,
                    login_form: PasswordMode = Body(..., title='')):
    user_token = await user_mgr.authorize(login_form, client, conn=conn)
    return OK(user_token)


@router.post('/password/code',
             summary='获取动态密码',
             response_model=Response)
async def create_password_code(client: Client,
                    conn: Conn,
                    password_code: PasswordCode = Body(..., title='body')):
    await user_mgr.create_user_password_code(password_code.username, password_code.password_type , client, conn=conn)
    return OK(None)
