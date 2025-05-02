#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> user
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/2 20:37
@Desc   ：
"""
import time
import random
from sqlalchemy import select
from app.routers.schemas import UserRegister
from app.routers.schemas import PasswordType
from app.routers.schemas import PasswordMode
from app.routers.schemas import Client
from app.routers.schemas import AccessToken
from app.common.utils import gm
from app.settings import settings, encrypt, decrypt
from app.predefine import errors
from app.predefine import AuthorizeFail
from app.models.user import User
from app.models.user import UserEmail
from app.models.user import UserMobile
from app.models.user import UserPasswordCode
from app.managers.base import get_by_pk


def validate_user_enabled(user: User):
    if not user.enabled:
        raise AuthorizeFail('user is unavailable')
    return user


async def get_enabled_user(pk: int, *, conn):
    user_obj = await get_by_pk(User, pk, error=AuthorizeFail('user is not exist'), conn=conn)
    validate_user_enabled(user_obj)
    return user_obj


async def get_user_or_none_by_username(related_model, username, *, conn: 'Session'):
    stmt = select(User).join(related_model).where(related_model.username == username)
    ret = await conn.execute(stmt)
    return ret.scalar_one_or_none()


async def get_enabled_user_by_username(related_model, username, *, conn: 'Session'):
    user_obj = await get_user_or_none_by_username(related_model, username, conn=conn)
    if user_obj is None:
        raise AuthorizeFail('{} is not exist'.format('user'))
    validate_user_enabled(user_obj)
    return user_obj



def verify_password(password, password_encrypt):
    return password_encrypt == gm.encrypt_sm3(password)


def create_user_token(user, client) -> AccessToken:
    expired_at = int(time.time()) + settings.token_expired_interval
    token = encrypt('{}::{}::{}'.format(user.id, client.client_id, expired_at))
    return AccessToken(token=token,
                       expired_at=expired_at,
                       user=user)

async def get_user_by_token(token, client: Client,  *, conn: 'Session'):
    try:
        plain = decrypt(token)
    except:
        raise AuthorizeFail('token is unavailable')
    else:
        tokens = plain.split('::')
        if len(tokens) != 3:
            raise AuthorizeFail('token is unavailable')
        try:
            user_id, client_id, expired_at = [int(token) for token in tokens]
            if expired_at < int(time.time()):
                raise AuthorizeFail('token is over expired')
            elif client_id != client.client_id:
                raise AuthorizeFail('client_id is unavailable')

            return await get_enabled_user(user_id, conn=conn)
        except:
            raise AuthorizeFail('token is unavailable')

    raise AuthorizeFail('token is unavailable')


async def authorize_by_password(password: PasswordMode,
                                client: Client,
                                *,
                                conn: 'Session') -> 'AccessToken':
    """
    登录
    :return:
    """
    match password.password_type:
        case PasswordType.EMAIL_PASSWORD | PasswordType.MOBILE_PASSWORD:
            related_model = UserEmail if password.password_type == PasswordType.EMAIL_PASSWORD else UserMobile
            user_obj = await get_enabled_user_by_username(related_model, password.username, conn=conn)
            if not verify_password(password.password, user_obj.password_encrypted):
                raise AuthorizeFail('password is unavailable')
        case PasswordType.EMAIL_CODE | PasswordType.MOBILE_CODE:
            user_pwd_code = await get_user_password_code(password.username, conn=conn)
            if user_pwd_code is None:
                raise AuthorizeFail('code is not exist')
            if user_pwd_code.code != password.password:
                raise AuthorizeFail('code is unavailable')

            if user_pwd_code.expired_at < time.time():
                raise AuthorizeFail('code is over expired')

            if user_pwd_code.client_id != client.client_id:
                raise AuthorizeFail('client_id is unavailable')

            user_obj = await get_enabled_user(user_pwd_code.user_id, conn=conn)
        case _:
            raise AuthorizeFail('password_type is not support yet')

    user_token = create_user_token(user_obj, client)
    return user_token


async def register(user: UserRegister, account_related_cls, *, conn: 'Session') -> None:
    user_obj = user.to_orm(User, exclude=['password_confirmed', 'username', 'password'])
    user_obj.password_encrypted = gm.encrypt_sm3(user.password)
    user_related = account_related_cls(username=user.username,
                                       user_id=user_obj.id)
    user_related.user = user_obj
    # user_related.id = await user_related.rebuild_id()

    # conn.add(user_obj)
    conn.add(user_related)
    await conn.commit()


async def get_user_password_code(username, *, conn: 'Session'):
    stmt = select(UserPasswordCode).where(UserPasswordCode.username == username).\
        limit(1).\
        order_by(UserPasswordCode.id.desc())
    ret = await conn.execute(stmt)
    return ret.scalar_one_or_none()


async def get_user_related_by_username(user_related_cls, username: str, *, conn: 'Session') -> UserEmail | UserMobile:
    stmt = select(user_related_cls).where(user_related_cls.username == username)
    ret = await conn.execute(stmt)
    user_related_obj = ret.scalar_one_or_none()
    if not user_related_obj:
        raise errors.DATA_NOT_EXIST('user is not exist')
    return user_related_obj


async def create_user_password_code0(username: str, user_id: int, client: Client, *, conn: 'Session'):
    code = ''.join(map(str, (random.randint(0, 9) for i in range(0, 6))))
    user_pwd_code = UserPasswordCode(username=username,
                                     user_id=user_id,
                                     code=code,
                                     client_id=client.client_id,
                                     client_ip=client.client_ip,
                                     expired_at=int(time.time()) + settings.code_expired_interval)
    user_pwd_code.id = await user_pwd_code.rebuild_id()
    conn.add(user_pwd_code)
    await conn.commit()
    return user_pwd_code


async def create_user_password_code(username: str, password_type: int, client: Client, *, conn: 'Session'):
    match password_type:
        case PasswordType.EMAIL_CODE.value:
            user_related = await get_user_related_by_username(UserEmail, username, conn=conn)
            user_password_code = await create_user_password_code0(username,
                                                                  user_related.user_id,
                                                                  client,
                                                                  conn=conn)
            # send email

        case PasswordType.MOBILE_CODE.value:
            user_related = await get_user_related_by_username(UserEmail, username, conn=conn)
            user_password_code = await create_user_password_code0(username,
                                                                  user_related.user_id,
                                                                  client, conn=conn)
            # send emsg
        case _:
            raise errors.DATA_VALIDATE_ERROR('password_type is not support yet')
