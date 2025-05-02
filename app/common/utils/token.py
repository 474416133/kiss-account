#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kylin-li-backend -> token
@IDE    ：PyCharm
@Author ：sven
@Date   ：2024/10/26 11:26
@Desc   ：
"""
import random
import time
import jwt


def create_token(payload, key, expire_in=7200):
    data = {
        'exp': int(time.time()) + expire_in,
        'payload': payload
    }
    return jwt.encode(data, key=key, algorithm="HS256")


def get_payload(token, key):
    return jwt.decode(
        token, key=key, leeway=random.randint(10, 20), algorithms=["HS256"]
    )['payload']

