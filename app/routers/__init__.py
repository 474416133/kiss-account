#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> __init__.py
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/1 20:30
@Desc   ：
"""
from . import api

def init_app(app):
    app.include_router(api.router)
