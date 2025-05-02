# -*- coding: utf-8 -*-
"""
model: logs
description:  
author: sven
date: 2022-09-04
"""
__author__ = '474416133@qq.com'

from logging import config, setLogRecordFactory, getLogRecordFactory
from app.common import vars
from app import logging_conf


old_factory = getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.trace_id = vars.trace_id_var.get()
    record.req_id = vars.req_id_var.get()
    return record




def init_app(app):
    setLogRecordFactory(record_factory)
    config.dictConfig(logging_conf.DEFAULT_LOGGING)

