# -*- coding: utf-8 -*-
"""
model: response
description:  
author: sven
date: 2022-09-11
"""
__author__ = '474416133@qq.com'
import math
from typing import Generic, TypeVar, Optional, List, Type
from pydantic import Field, BaseModel
# from pydantic.generics import GenericModel

DataType = TypeVar('DataType')


class Response(BaseModel, Generic[DataType]):
    err_code: int = 0
    err_msg: str = 'OK'
    data: Optional[DataType] = None


class Page(BaseModel, Generic[DataType]):
    """
    page对象
    """
    page_size: int = 10
    page: int = 1
    total_records: int = 0
    total_pages: int = 0
    has_next: bool = False
    records: List[DataType] = Field(default_factory=list)

    @classmethod
    def construct(cls: Type['Model'],
                  records: List[DataType],
                  total_records:int,
                  page_size: int= 10,
                  page:int = 1) -> 'Model':
        """
        @override
        :param _fields_set:
        :param values:
        :return:
        """
        instance = super().construct(None,
                                     records=records,
                                     total_records=total_records,
                                     page_size=page_size,
                                     page=page)
        instance.total_pages = math.ceil(instance.total_records / instance.page_size)
        instance.has_next = instance.total_pages > instance.page
        return instance


def OK(data, msg='OK'):
    """
    成功
    :param data:
    :param msg:
    :return:
    """
    return Response(err_code=0, err_msg=msg, data=data)


def Fail(err_code, err_msg='error', data=None):
    """
    失败
    :param err_code:
    :param err_msg:
    :param data:
    :return:
    """
    return Response(err_code=err_code, err_msg=err_msg, data=data)


def create_page(records, total_records=None, page_size=10, page=1, msg='OK'):
    """
    :param records:
    :param total_records:
    :param page_size:
    :param page:
    :return:
    """
    total_records = len(records) if total_records is None else total_records
    page_instance = Page.construct(records=records,
                                   total_records=total_records,
                                   page_size=page_size,
                                   page=page)

    return OK(page_instance, msg)

