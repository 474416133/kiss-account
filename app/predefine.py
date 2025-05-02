#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：game-web -> predefine
@IDE    ：PyCharm
@Author ：sven
@Date   ：2024/7/3 20:39
@Desc   ：
"""
import enum
from app.common.errors import IError
from app.common.errors import BizError


@enum.unique
class errors(IError):
    DATA_VALIDATE_ERROR = 4000
    DATA_NOT_EXIST = 5000
    AUTHORIZE_FAIL = 5001
    USER_DISABLED = 5002
    ORDER_MONEY_ERROR = 6000
    ITEM_NOT_ENOUGH = 6100
    NOT_ITEM_OWNER = 6101



# UNAUTHORIZED
class AuthorizeFail(BizError):
    
    def __init__(self, error_remark=None, *, request=None):
        super().__init__(errors.AUTHORIZE_FAIL.value, errors.AUTHORIZE_FAIL.name, error_remark, request=request)

