#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> __init__.py
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/3 1:23
@Desc   ：
"""
from fastapi import APIRouter

router = APIRouter(prefix='/users')


from . import v1
router.include_router(v1.router)