#!/usr/bin/env python

import asyncio
import logging.config

import websockets
from aioredis import create_connection, Channel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
redis_channel = 'ping-users'
USERS = set()


async def redis_subscribe(path):
    conn = await create_connection(('localhost', 6379))
    # Set up a subscribe channel
    channel = Channel(redis_channel, is_pattern=False)
    await conn.execute_pubsub('subscribe', channel)
    return channel, conn


async def redis_get_message(channel):
    logger.debug('start: redis_get_message')
    message = await channel.get()
    logger.debug(f'finish: redis_get_message, message: {message}')
    return message


async def my_ws_consumer(message):
    logger.debug(f'my_consumer: {message}')
    await asyncio.sleep(1)


async def ws_consumer_handler(websocket, path):
    async for message in websocket:
        await my_ws_consumer(message)


async def producer_handler(websocket, message):
    logger.debug(f'producer_handler: {message}')
    await websocket.send(message)


async def register(websocket):
    USERS.add(websocket)
    logger.debug(f'+++ register {websocket}')


async def browser_server(websocket, path):
    # laczy sie do redisa przy kazdym polaczonym kliencie ws
    # nie zwalnia polaczen
    channel, conn = await redis_subscribe(path)
    logger.debug(f'channel: {channel}, conn: {conn}')

    await register(websocket)
    try:
        while True:
            logger.debug(f'while True')

            ws_consumer_task = asyncio.create_task(ws_consumer_handler(websocket, path))
            # ws_register_task = register(websocket)
            redis_task = asyncio.create_task(redis_get_message(channel))
            done, pending = await asyncio.wait(
                [ws_consumer_task, redis_task, ], return_when=asyncio.FIRST_COMPLETED, )

            for task in pending:
                task.cancel()

            if redis_task.done():
                logger.debug('redis_task.done():')
                message = redis_task.result()
                await producer_handler(websocket, message.decode('utf-8'))
            else:
                logger.debug('!redis_task.done():')

    except websockets.exceptions.ConnectionClosed:
        # Free up channel if websocket goes down
        logger.debug('websockets.exceptions.ConnectionClosed')
        await conn.execute_pubsub('unsubscribe', channel)
        conn.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    ws_server = websockets.serve(browser_server, 'localhost', 6789)
    loop.run_until_complete(ws_server)
    loop.run_forever()
