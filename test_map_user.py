import random
import unittest
from pprint import pprint

from map_user import MapUser

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestMapUser(unittest.TestCase):
    def setUp(self):
        self.map_user = MapUser()
        self.map_uid_ws = {}  # uid can have many websocket
        self.map_ws_uid = {}  # one websocket for one uid

    def test_add_uid(self):
        # split to more tests?

        map_user = self.map_user
        uid_1 = random.randint(1, 100)
        ws_id_1 = random.randint(1, 100)
        ws_1 = f'websocket_{ws_id_1}_for_{uid_1}'
        map_uid_ws = {uid_1: set((ws_1,))}
        map_ws_uid = {ws_1: uid_1}
        map_user.register_user(uid_1, ws_1)
        self.assertEqual(map_user.map_uid_ws, map_uid_ws)
        self.assertEqual(map_user.map_ws_uid, map_ws_uid)

        ws_id_2 = random.randint(1, 100)
        ws_2 = f'websocket_{ws_id_2}_for_{uid_1}'
        map_uid_ws = {
            uid_1: set((ws_1, ws_2,)),
        }
        map_ws_uid = {
            ws_1: uid_1,
            ws_2: uid_1,
        }
        map_user.register_user(uid_1, ws_2)
        self.assertEqual(map_user.map_uid_ws, map_uid_ws, 'check map_uid_ws')
        self.assertEqual(map_user.map_ws_uid, map_ws_uid, 'check map_ws_uid')

        uid_2 = random.randint(1, 100)
        ws_id_3 = random.randint(1, 100)
        ws_3 = f'websocket_{ws_id_3}_for_{uid_2}'

        map_uid_ws = {
            uid_1: set((ws_1, ws_2,)),
            uid_2: set((ws_3,))
        }
        map_ws_uid = {
            ws_1: uid_1,
            ws_2: uid_1,
            ws_3: uid_2,
        }
        map_user.register_user(uid_2, ws_3)
        self.assertEqual(map_user.map_uid_ws, map_uid_ws, 'check map_uid_ws')
        self.assertEqual(map_user.map_ws_uid, map_ws_uid, 'check map_ws_uid')
        # pprint(map_uid_ws)
        # pprint(map_ws_uid)
        # pprint(map_user.map_uid_ws)
        # pprint(map_user.map_ws_uid)

        list_ws_1 = map_user.get_ws_set_by_uid([uid_1])
        self.assertEqual(list_ws_1, set((ws_1, ws_2)), 'get_ws_set_by_uid')

        list_ws_2 = map_user.get_ws_set_by_uid([uid_2])
        self.assertEqual(list_ws_2, set((ws_3,)), 'get_ws_set_by_uid')

        list_ws_3 = map_user.get_ws_set_by_uid([uid_1, uid_2])
        # pprint(list_ws_3)
        # pprint(set((ws_1, ws_2, ws_3)))
        self.assertEqual(list_ws_3, set((ws_1, ws_2, ws_3)), 'get_ws_set_by_uid')

        map_uid_ws = {
            uid_1: set((ws_1,)),
            uid_2: set((ws_3,))
        }
        map_ws_uid = {
            ws_1: uid_1,
            ws_3: uid_2,
        }
        map_user.unregister_user_by_ws(ws_2)
        self.assertEqual(map_user.map_uid_ws, map_uid_ws, 'check map_uid_ws')
        self.assertEqual(map_user.map_ws_uid, map_ws_uid, 'check map_ws_uid')

        map_uid_ws = {
            uid_1: set((ws_1,)),
        }
        map_ws_uid = {
            ws_1: uid_1,
        }
        map_user.unregister_user_by_ws(ws_3)

        self.assertEqual(map_user.map_uid_ws, map_uid_ws, 'check map_uid_ws')
        self.assertEqual(map_user.map_ws_uid, map_ws_uid, 'check map_ws_uid')


if __name__ == '__main__':
    unittest.main()
