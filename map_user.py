import logging
from pprint import pformat

logger = logging.getLogger(__name__)


class MapUser:
    def __init__(self):
        self.map_ws_uid = {}  # one websocket for one uid
        self.map_uid_ws = {}  # uid can have many websocket

    def register_user(self, uid, ws):
        logger.debug(f'register_user ({uid}, {ws})')
        self.map_ws_uid[ws] = uid
        current = self.map_uid_ws.setdefault(uid, set())
        current.add(ws)
        self.map_uid_ws[uid] = current

    def unregister_user(self, uid, ws):
        logger.debug(f'unregister_user ({uid}, {ws})')
        self.map_ws_uid.pop(ws, None)
        current = self.map_uid_ws.get(uid)
        if current:
            current.remove(ws)
            print(f'current = {current}')
            if not current:
                self.map_uid_ws.pop(uid, None)
                print(f'empty current = {current}')
                print(self.map_uid_ws)
            else:
                print(f'current? = {current}')

    def unregister_user_by_ws(self, ws):
        logger.debug(f'unregister_user_by_ws ({ws})')
        uid = self.map_ws_uid.get(ws)
        if uid:
            self.unregister_user(uid, ws)
        else:
            logger.error(f"can't find uid for ws: {ws}")

    def get_ws_set_by_uid(self, uids: list):
        logger.debug(f'unregister_user_by_ws ({uids})')
        all_ws = set()
        for uid in uids:
            all_ws.update(self.map_uid_ws.get(uid))
        return all_ws

    def dump(self):
        logger.debug('-------------------------')
        logger.debug('map_ws_uid')
        logger.debug(pformat(self.map_ws_uid))
        logger.debug('map_uid_ws')
        logger.debug(pformat(self.map_uid_ws))
        logger.debug('-------------------------')


if __name__ == '__main__':
    map_user = MapUser()

    map_user.register_user(1, 'abc')
    map_user.dump()
    map_user.register_user(2, 'def')
    map_user.dump()
    map_user.register_user(1, 'zxc')
    map_user.dump()

    map_user.unregister_user(1, 'abc')
    map_user.dump()
    map_user.unregister_user(2, 'def')
    map_user.dump()
    map_user.unregister_user(1, 'zxc')
    map_user.dump()
    map_user.unregister_user(1, 'zxc')
    map_user.dump()
    map_user.unregister_user(1, 'zxc')
    map_user.dump()
