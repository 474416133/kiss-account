# -*- coding: utf-8 -*-
"""
model: log_config
description:  
author: sven
date: 2022-09-04
"""
from app.settings import settings
__author__ = '474416133@qq.com'
LOG_PATH = settings.logging.path
print('LOG_PATH: {}'.format(LOG_PATH))


DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        # 日志格式
        'verbose': {
            'format': '[%(asctime)s] [%(name)s] [%(module)s:%(funcName)s:%(lineno)d] '
                      '[%(levelname)s] [%(req_id)s] [%(trace_id)s]- %(message)s'},
        'simple': {  # 简单格式
            'format': '%(message)s'
        },
    },
    # 过滤
    'filters': {
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'web': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '{}/web.log'.format(LOG_PATH),
            'when': 'D',  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'verbose',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '{}/sql.log'.format(LOG_PATH),
            'when': 'D',  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'verbose',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '{}/error.log'.format(LOG_PATH),
            'when': 'D',  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'verbose',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },

        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'kiss-account': {
            'handlers': ['web', 'console', 'error'],
            'level': 'DEBUG',
            'propagate': False
        },
        # log 调用时需要当作参数传入
        'error': {
            'handlers': ['error', 'console'],
            'level': 'ERROR',
            'propagate': False
        },

        'sqlalchemy.engine': {
            'handlers': ['sql', 'console', 'error'],
            'level': 'INFO',
            'propagate': False
        },

    }
}