# -*- coding: utf-8 -*-
"""
model: vars
description:  
author: sven
date: 2022-11-05
"""
__author__ = '474416133@qq.com'
from contextvars import ContextVar


trace_id_var = ContextVar('trace_id', default=None)
req_id_var = ContextVar('req_id', default=None)
