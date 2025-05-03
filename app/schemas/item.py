#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：kiss-account -> item
@IDE    ：PyCharm
@Author ：sven
@Date   ：2025/5/3 22:39
@Desc   ：
"""
from typing import Optional
from typing import List

from pydantic import  Field, model_validator, field_validator
from .base import SAModelBase



class SubItemIn(SAModelBase):
    item_id: int = Field(..., title='物品id')
    item_num: int = Field(..., gt=0, title='物品数量')


class ItemIn(SAModelBase):

    name: str = Field(..., title='物品名称')
    price: int = Field(..., title='物品价格')
    picture_url: str = Field(..., title='物品图像url')
    tags: Optional[List[str]] = Field(default_factory=list, title='标签')
    on_sale: bool = Field(True, title='是非上架')
    sale_cate: Optional[int] = Field(None, title='上架目录')
    remark: str = Field(..., title='物品备注')
    extra_data: dict| None = Field(None, title='额外数据')
    items: Optional[List[SubItemIn]] = Field(default_factory=list, title='物品类型')


class UserItemOut(SAModelBase):

    id: int
    item_name: str = Field(..., title='物品名称')
    item_type: int = Field(..., title='物品类型')
    item_num: int = Field(..., title='物品数量')
    item_picture_url: str = Field(..., title='物品数量')
    item_num_used: int = Field(..., title='物品已数量')
