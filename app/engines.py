# -*- coding: utf-8 -*-
"""
model: engines
description:  
author: sven
date: 2022-09-09
"""
__author__ = '474416133@qq.com'

import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from  app.settings import settings, get_database_dsn


def create_engine(db_options):
    """
    创建
    :param db_options:
    :return:
    """
    # 更新options
    """
    https://docs.sqlalchemy.org/en/14/dialects/postgresql.html?highlight=asyncpg#module-sqlalchemy.dialects.postgresql.asyncpg
    
    Disabling the PostgreSQL JIT to improve ENUM datatype handling
    engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/tmp",
    connect_args={"server_settings": {"jit": "off"}},
    )
    """
    # options['server_settings'] = {"jit": "off"}
    options = settings.database.options
    options['future'] = True
    return create_async_engine(get_database_dsn(), **options)


engine = create_engine(settings.database)
Session = async_scoped_session(sessionmaker(engine, class_=AsyncSession, expire_on_commit=False),
                               scopefunc=asyncio.current_task)

