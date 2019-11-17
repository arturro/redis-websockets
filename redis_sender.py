#!/usr/bin/env python

import asyncio
import logging.config
import random

import aioredis

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
redis_channel = 'ping-users'


async def main(redis_channel):
    pub = await aioredis.create_redis('redis://localhost')
    data = {
        'type': 'state',
        'value': "{}".format(int(random.random() * 10))
    }
    res = await pub.publish_json(redis_channel, data)
    logger.debug(f'send to: {res} subscribers')
    pub.close()


if __name__ == '__main__':
    asyncio.run(main(redis_channel))
