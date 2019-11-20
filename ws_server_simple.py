#!/usr/bin/env python

import asyncio
import json
import logging.config

import aioredis
import websockets

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
redis_channel = 'ping-users'
USERS = set()


async def register(websocket):
    USERS.add(websocket)
    logger.debug(f'registered: {USERS}')


async def unregister(websocket):
    USERS.remove(websocket)
    logger.debug(f'registered: {USERS}')


async def browser_server(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            logging.error(f'event: {data}')
    finally:
        await unregister(websocket)


async def handle_msg(msg):
    logger.debug(f'Got Message: {msg}')
    msg = json.dumps(msg)
    for websocket in USERS:
        logger.debug(f'prepare to send {websocket}')
        await websocket.send(msg)
        logger.debug(f'send to {websocket}')
    logger.debug('End sleep')


async def reader(ch):
    while True:
        await ch.wait_message()
        msg = await ch.get_json()
        logger.debug(f'reader msg: {msg}')
        asyncio.create_task(handle_msg(msg))


async def redis_main():
    sub = await aioredis.create_redis(('localhost', 6379))
    res = await sub.subscribe(redis_channel)
    ch1 = res[0]
    tsk = await reader(ch1)
    await sub.unsubscribe('chan:1')
    sub.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    ws_server = websockets.serve(browser_server, 'localhost', 6789)
    loop.run_until_complete(ws_server)
    loop.run_until_complete(redis_main())
    loop.run_forever()
