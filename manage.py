#!/usr/bin/env python

from backend.log import log
from backend.app import app
from backend.app import start_app

backend = app

@backend.on_event("startup")
async def app_startup():
    await start_app()
    log.info('Starting Application ....')

@backend.on_event("shutdown")
async def app_shutdown():
    log.info('Stopping Application, Please wait ....')