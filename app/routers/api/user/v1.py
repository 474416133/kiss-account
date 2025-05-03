#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> v1
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/3 1:23
@Desc   ：
"""
import logging
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Query
from app.common.responses import Response, OK
from app.schemas.user import UserRegister
from app.schemas.authorize import User
from app.schemas.user import UserPassword
from app.schemas.authorize import PasswordType
from app.managers import user as user_mgr
from app.routers.depends import Token
from app.routers.depends import CurrentUser
from app.routers.depends import authenticated
from app.routers.depends import Client, Conn


logger = logging.getLogger('web')
router = APIRouter(prefix='/v1')


@router.post('/account',
             summary='创建账号',
             tags=['用户'],
             response_model=Response[User])
async def create_account(conn: Conn,
                         client: Client,
                         user: UserRegister = Body(..., title='注册信息')):
    await user_mgr.register(user, conn=conn)
    return OK(None)


@router.get('/account/me',
            summary='获取个人信息',
            tags=['用户'],
            response_model=Response[User],
            dependencies=[Depends(authenticated)])
async def get_me(
                 client: Client,
                 token: Token,
                 user: CurrentUser):
    logger.debug(f'client_id: {client.client_id}, client_ip: {client.client_ip}, token； {token}')
    return OK(user)


@router.patch('/account/password',
             summary='修改密码',
              tags=['用户'],
             response_model=Response,
              dependencies=[Depends(authenticated)])
async def change_password(conn: Conn,
                         client: Client,
                         user: CurrentUser,
                         user_password: UserPassword = Body(..., title='注册信息'),
                         ):
    await user_mgr.change_user_password(user, user_password, client,  conn=conn)
    return OK(None)


@router.post('/account/password/code',
             summary='用户动态code',
             tags=['用户', '授权'],
             response_model=Response,
              dependencies=[Depends(authenticated)])
async def create_password_code(conn: Conn,
                         client: Client,
                         user: CurrentUser,
                         password_type: PasswordType = Query(..., title='code类型')
                         ):
    await user_mgr.create_user_password_code_by_user(user, password_type, client, conn=conn)
    return OK(None)
