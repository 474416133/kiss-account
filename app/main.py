# -*- coding: utf-8 -*-
"""
model: main
description:  
author: sven
date: 2022-09-13
"""
__author__ = '474416133@qq.com'
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.common import vars
from app import settings
from app import logs
from app import engines
from app import exception_handlers
from app import routers


@asynccontextmanager
async def lifespan(app):

    print('setuped....')
    yield
    await engines.Session.close()
    print('teardown....')


logger = logging.getLogger('kiss-account')
app = FastAPI(lifespan=lifespan)
exception_handlers.init_app(app)
logs.init_app(app)
routers.init_app(app)


@app.middleware("http")
async def get_app_var(request: Request, call_next):
    start_time = time.time()

    vars.req_id_var.set(id(request))
    vars.trace_id_var.set(request.headers.get('X-TRACE-ID'))

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info('{} {} {}'.format(request.method, request.url, process_time))
    # 设置 lang

    return response


if __name__ == '__main__':

    import uvicorn
    uvicorn.run('app.main:app',
                host='127.0.0.1',
                port=8000,
                workers=settings.settings.workers,
                reload=settings.DEBUG)
