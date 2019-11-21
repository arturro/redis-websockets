#!/usr/bin/env python

import asyncio
import argparse
import logging.config
import random

import aioredis

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
redis_channel = 'ping-users'


async def main(redis_channel, uids):
    pub = await aioredis.create_redis('redis://localhost')
    """
    data = {
        'type': 'state',
        'value': '{}'.format(int(random.random() * 10)),
        'uids': uids,
    }
    """
    data = {
        'type': 'ping',
        'uids': uids,
    }
    res = await pub.publish_json(redis_channel, data)
    logger.debug(f'send to: {res} subscribers')
    pub.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send ping to users.')
    parser.add_argument('uids', metavar='N', type=str, nargs='+',
                        help='uids for ping')

    args = parser.parse_args()
    uids = args.uids
    asyncio.run(main(redis_channel, uids))
