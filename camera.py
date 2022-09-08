

class Camera:
    def __init__(self, map, x: int = 0, y: int = 0) -> None:
        self.x, self.y = x, y
        self.map = map

    @property
    def pos_x(self):
        return self.x

    @pos_x.setter
    def pos_x(self, n):
        self.x = n

    @property
    def pos_y(self):
        return self.y

    @pos_y.setter
    def pos_y(self, n):
        self.y = n
