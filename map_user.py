class MapUser:
    """
        add description

        self.map_ws_uid = {}  # one websocket for one uid
        self.map_uid_ws = {}  # uid can have many websocket
    """

    def __init__(self):
        self.map_ws_uid = {}
        self.map_uid_ws = {}

    def register_user(self, uid, ws):
        #  TODO swap uid<>ws and uid=0?
        self.map_ws_uid[ws] = uid
        current = self.map_uid_ws.setdefault(uid, set())
        current.add(ws)
        self.map_uid_ws[uid] = current

    def unregister_user(self, uid, ws):
        self.map_ws_uid.pop(ws, None)
        current = self.map_uid_ws.get(uid)
        if current:
            current.remove(ws)
            if not current:
                self.map_uid_ws.pop(uid, None)

    def unregister_user_by_ws(self, ws):
        uid = self.map_ws_uid.get(ws)
        if uid:
            self.unregister_user(uid, ws)

    def get_ws_set_by_uid(self, uids=[]):
        all_ws = set()
        if uids:
            for uid in uids:
                ws = self.map_uid_ws.get(uid)
                if ws:
                    all_ws.update(ws)
        else:
            all_ws = set(self.map_ws_uid.keys())
        return all_ws
