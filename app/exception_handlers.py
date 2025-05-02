# -*- coding: utf-8 -*-
"""
model: exception_handlers
description:  
author: sven
date: 2022-11-03
"""
__author__ = '474416133@qq.com'
import logging
from fastapi.exceptions import StarletteHTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from app.common.errors import BizError
from app.common.responses import Fail
from app.predefine import errors


logger = logging.getLogger('kiss-account')


# @app.exception_handler(StarletteHTTPException)
async def handle_http_except(request, exc):
    logger.exception('http error.')
    return JSONResponse(Fail(err_code=exc.status_code, err_msg=exc.detail).dict(),
                         status_code=exc.status_code,
                         headers=exc.headers)


# @app.exception_handler(RequestValidationError)
async def handle_validator_except(request, exc):
    logger.exception('validate error.')
    return JSONResponse(Fail(err_code=422, err_msg="数据校验错误", data=exc.body).dict(),
                         status_code=422)


# @app.exception_handler(ValueError)
async def handle_value_except(request, exc):
    logger.exception('validate[value] error.')
    return JSONResponse(Fail(err_code=400, err_msg=str(exc)).dict(),
                         status_code=400)


# @app.exception_handler(BizError)
async def handle_biz_except(request, exc):
    logger.exception('biz error.')
    status_code = 500
    if exc.error_code == errors.AUTHORIZE_FAIL.value:
        status_code = 401

    return JSONResponse(Fail(err_code=exc.error_code,
                             err_msg=exc.error_value,
                             data=exc.as_dict()).dict(),
                        status_code=status_code)


# @app.exception_handler(Exception)
async def handle_except(request, exc):
    logger.exception('unknown error.')
    return JSONResponse(Fail(err_code=500,
                err_msg='服务器内部错误').dict(),
                         status_code=500)


def init_app(app):
    """

    :param app:
    :return:
    """
    app.add_exception_handler(StarletteHTTPException, handle_http_except)
    app.add_exception_handler(RequestValidationError, handle_validator_except)
    app.add_exception_handler(ValueError, handle_value_except)
    app.add_exception_handler(BizError, handle_biz_except)
    app.add_exception_handler(Exception, handle_except)