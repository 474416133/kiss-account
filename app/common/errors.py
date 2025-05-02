#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ： errors
@IDE    ：PyCharm
@Author ：sven
@Date   ：2022/2/26 12:51
@Desc   ：
"""

import enum
from enum import Enum


class BizError(RuntimeError):
    """
    业务异常
    """
    __slots__ = "error_code", "error_value", "error_remark"

    def __init__(self, error_code, error_value, error_remark=None, *, request: 'Request' = None):
        self.error_code = error_code
        self.error_value = error_value
        self.error_remark = error_remark or self.error_value
        self.request = request

    def __str__(self):
        """
        @overide
        :return:
        """
        return f"error_code={self.error_code}," \
               f" error_value={self.error_value}," \
               f" error_remark={self.error_remark}"

    def as_dict(self):
        """

        :return:
        """
        return {
            "error_code" : self.error_code,
            "error_value" :self.error_value,
            "error_remark" : self.error_remark
        }


class IError(Enum):
    """
    异常
    """
    def exception(self, error_remark=None, *, request=None):
        """
        异常
        :param msg:
        :param args:
        :return: BizError对象
        """
        return BizError(self.value, self.name, error_remark, request=request)

    def __call__(self, error_remark=None, *,  request=None):
        return self.exception(error_remark, request=request)



