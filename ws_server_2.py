#!/usr/bin/env python

import asyncio
import json
import logging.config

import aioredis
import websockets

from map_user import MapUser

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
redis_channel = 'ping-users'


def register(websocket, uid):
    map_user.register_user(uid, websocket)


def unregister(websocket):
    map_user.unregister_user_by_ws(websocket)


def dispatch_ws_action(websocket, data):
    logging.error(f'event: {data}')
    action = data.get('action')
    if action == 'register':
        uid = data.get('uid')
        if uid:
            register(websocket, uid)
        else:
            logger.debug(f'unknown uid for {data}')
    else:
        logger.debug(f'unknown action for {data}')


async def browser_server(websocket, path):
    # await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            dispatch_ws_action(websocket, data)
    finally:
        unregister(websocket)


async def ping_users(msg):
    data = {'type': 'state', 'value': msg.get('value')}
    logger.debug(map_user.get_ws_set_by_uid(msg.get('uids')))

    for websocket in map_user.get_ws_set_by_uid(msg.get('uids')):
        logger.debug(f'prepare to send {websocket}')
        # await asyncio.sleep(1)
        await websocket.send(json.dumps(data))
        logger.debug(f'send to {websocket}')


async def redis_handle_msg(msg):
    logger.debug(f'Got Message: {msg}')
    await ping_users(msg)
    logger.debug('End sleep')


async def redis_reader(ch):
    while True:
        await ch.wait_message()
        msg = await ch.get_json()
        logger.debug(f'reader msg: {msg}')
        asyncio.create_task(redis_handle_msg(msg))


async def redis_main():
    sub = await aioredis.create_redis(('localhost', 6379))
    res = await sub.subscribe(redis_channel)
    ch1 = res[0]
    tsk = await redis_reader(ch1)
    await sub.unsubscribe('chan:1')
    sub.close()


map_user = MapUser()  # TODO move from global to class?

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    ws_server = websockets.serve(browser_server, 'localhost', 6789)
    loop.run_until_complete(ws_server)
    loop.run_until_complete(redis_main())
    loop.run_forever()
