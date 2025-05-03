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
from app.routers.schemas import UserPassword
from app.routers.schemas import Client
from app.routers.schemas import AccessToken
from app.common.utils import gm
from app.common.utils import date
from app.settings import settings, encrypt, decrypt
from app.predefine import errors
from app.predefine import AuthorizeFail
from app.models.user import User
from app.models.user import UserEmail
from app.models.user import UserMobile
from app.models.user import UserPasswordCode
from app.managers.base import get_by_pk, update_by_pk


def validate_user_enabled(user: User):
    if not user.enabled:
        raise AuthorizeFail('user is unavailable')
    return user


async def get_enabled_user(pk: int, *, conn):
    user_obj = await get_by_pk(User, pk, error=AuthorizeFail('user is not exist'), conn=conn)
    validate_user_enabled(user_obj)
    return user_obj


async def get_user_or_none_by_username(username, *, conn: 'Session'):
    stmt = select(User).where(User.username == username)
    ret = await conn.execute(stmt)
    return ret.scalar_one_or_none()


async def get_enabled_user_by_username(username, *, conn: 'Session'):
    user_obj = await get_user_or_none_by_username(username, conn=conn)
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


def validate_password_code(password_code: UserPasswordCode, code: str, client: Client):
    if password_code is None:
        raise AuthorizeFail('code is not exist')
    if password_code.code != code:
        raise AuthorizeFail('code is unavailable')

    if password_code.expired_at < time.time():
        raise AuthorizeFail('code is over expired')

    if password_code.client_id != client.client_id:
        raise AuthorizeFail('client_id is unavailable')


async def authorize_by_code(user_related_model,
                            password: PasswordMode,
                            client: Client,
                            *,
                            conn: 'Session'):
    user_pwd_code = await get_user_password_code(password.username, conn=conn)
    validate_password_code(user_pwd_code, password.password, client)

    if user_pwd_code.user_id:
        user_obj = await get_enabled_user(user_pwd_code.user_id, conn=conn)
    else:
        user_obj = User(username=password.username,
                        last_login_ip=client.client_ip,
                        nickname=password.username,
                        avatar_url='default.png')
        user_related_obj = user_related_model(username=password.username,
                                              activated=True,
                                              activate_at=date.now(),
                                              activate_ip=client.client_ip)
        user_related_obj.user = user_obj
        conn.add(user_related_obj)
        await conn.commit()
    return user_obj


async def authorize(password: PasswordMode,
                                client: Client,
                                *,
                                conn: 'Session') -> 'AccessToken':
    """
    登录
    :return:
    """
    match password.password_type:
        case PasswordType.PASSWORD:
            user_obj = await get_enabled_user_by_username(password.username, conn=conn)
            if not verify_password(password.password, user_obj.password_encrypted):
                raise AuthorizeFail('password is unavailable')
        case PasswordType.EMAIL_CODE:
            user_obj = await authorize_by_code(UserEmail, password, client, conn=conn)
        case PasswordType.EMAIL_CODE:
            user_obj = await authorize_by_code(UserMobile, password, client, conn=conn)
        case _:
            raise AuthorizeFail('password_type is not support yet')


    user_token = create_user_token(user_obj, client)
    return user_token


async def register(user: UserRegister, *, conn: 'Session') -> None:
    user_obj = user.to_orm(User, exclude=['password_confirmed', 'password'])
    user_obj.password_encrypted = gm.encrypt_sm3(user.password)
    conn.add(user_obj)
    # conn.add(user_related)
    await conn.commit()
    return user_obj


async def get_user_password_code(username, *, conn: 'Session'):
    stmt = select(UserPasswordCode).where(UserPasswordCode.username == username).\
        limit(1).\
        order_by(UserPasswordCode.id.desc())
    ret = await conn.execute(stmt)
    return ret.scalar_one_or_none()

async def get_user_password_code_by_userid(userid, *, conn: 'Session'):
    stmt = select(UserPasswordCode).where(UserPasswordCode.user_id == userid).\
        limit(1).\
        order_by(UserPasswordCode.id.desc())
    ret = await conn.execute(stmt)
    return ret.scalar_one_or_none()


async def get_user_related_by_username(user_related_cls, username: str, *, conn: 'Session') -> UserEmail | UserMobile:
    stmt = select(user_related_cls).where(user_related_cls.username == username)
    ret = await conn.execute(stmt)
    return ret.scalar_one_or_none()



async def get_user_related_by_userid(user_related_cls, user_id: int, *, conn: 'Session') -> UserEmail | UserMobile:
    stmt = select(user_related_cls).where(user_related_cls.user_id == user_id)
    ret = await conn.execute(stmt)
    return ret.scalar_one_or_none()



async def create_user_password_code0(username: str, user_id: int, client: Client, *, conn: 'Session'):
    code = ''.join(map(str, (random.randint(0, 9) for i in range(0, 6))))
    user_pwd_code = UserPasswordCode(username=username,
                                     user_id=user_id,
                                     code=code,
                                     client_id=client.client_id,
                                     client_ip=client.client_ip,
                                     expired_at=int(time.time()) + settings.code_expired_interval)
    conn.add(user_pwd_code)
    await conn.commit()
    return user_pwd_code

async def create_user_password_code_by_email(user_related: UserEmail, client: Client, *, conn: 'Session'):
    user_password_code = await create_user_password_code0(user_related.username,
                                                          user_related.user_id if user_related else None,
                                                          client,
                                                          conn=conn)
    # send email



async def create_user_password_code_by_mobile(user_related: UserMobile, client: Client, *, conn: 'Session'):
    user_password_code = await create_user_password_code0(user_related.username,
                                                          user_related.user_id if user_related else None,
                                                          client,
                                                          conn=conn)
    # send mobile



async def create_user_password_code(username: str, password_type: PasswordType, client: Client, *, conn: 'Session'):
    created = False
    match password_type:
        case PasswordType.EMAIL_CODE:
            user_related = await get_user_related_by_username(UserEmail, username, conn=conn)
            if user_related:
                await create_user_password_code_by_email(user_related, client, conn=conn)
                created = True


        case PasswordType.MOBILE_CODE:
            user_related = await get_user_related_by_username(UserEmail, username, conn=conn)
            if user_related:
                await create_user_password_code_by_mobile(user_related, client, conn=conn)
                created = True

        case _:
            raise errors.DATA_VALIDATE_ERROR('password_type is not support yet')

    if not created:
        raise errors.DATA_VALIDATE_ERROR('password_type is not support yet')


async def create_user_password_code_by_user(user: User, password_type: PasswordType, client: Client, *, conn: 'Session'):
    created = False
    match password_type:
        case PasswordType.EMAIL_CODE:
            user_related = await get_user_related_by_userid(UserEmail, user.id, conn=conn)
            if user_related:
                await create_user_password_code_by_email(user_related, client, conn=conn)
                created = True


        case PasswordType.MOBILE_CODE:
            user_related = await get_user_related_by_userid(UserMobile, user.id, conn=conn)
            if user_related:
                await create_user_password_code_by_mobile(user_related, client, conn=conn)
                created = True

        case _:
            raise errors.DATA_VALIDATE_ERROR('password_type is not support yet')

    if not created:
        raise errors.DATA_VALIDATE_ERROR('password_type is not support yet')


async def change_user_password(user: User,
                               password: UserPassword,
                               client: Client,
                               *,
                               conn: 'Session'):
    match password.password_type0:
        case PasswordType.PASSWORD:
            if not verify_password(password.code_or_password0, user.password_encrypted):
                raise AuthorizeFail('旧密码验证失败')

        case PasswordType.EMAIL_CODE|PasswordType.MOBILE_CODE:
            user_password_code = get_user_password_code_by_userid(user.id, conn=conn)
            validate_password_code(user_password_code, password.code_or_password0, client)
        case _:
            raise AuthorizeFail('不支持的密码类型')

    user.password_encrypted = gm.encrypt_sm3(password.password)
    await update_by_pk(User, user.id, {'password_encrypted': user.password_encrypted, 'modified_at': date.now()}, conn=conn)





