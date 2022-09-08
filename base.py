import random


class RoomBase:
    def __init__(self, file_name) -> None:
        self._file_name = file_name
        self.rooms = []

    @property
    def len_rooms(self):
        return len(self.rooms)

    def add(self, room):
        self.rooms.append(room)

    def id_get(self, id):
        for r in self.rooms:
            if r.id == id:
                return r
        return None

    def random(self):
        return self.rooms[random.randint(0, len(self.rooms) - 1)]

    def find_id(self, x, y, t):
        for r in self.rooms[1:]:
            if r.plan[y][x] == t and len(r.get(x, y)) == 0:
                return r.id
        return -1
