#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> __init__.py
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/1 20:35
@Desc   ：
"""
from fastapi import APIRouter

from . import user
from . import oauth2


router = APIRouter(prefix='/api')
router.include_router(user.router)
router.include_router(oauth2.router)
