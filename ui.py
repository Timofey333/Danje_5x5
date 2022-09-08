from logging import getLevelName
from game_objects import get_unique_id, selection
import pygame
import math
import settings


class ui_images:
    folder = "images/ui/"

    clock_0 = folder + "clock/clock_0.png"
    clock_1 = folder + "clock/clock_1.png"
    clock_2 = folder + "clock/clock_2.png"
    clock_3 = folder + "clock/clock_3.png"
    clock_4 = folder + "clock/clock_4.png"
    clock_5 = folder + "clock/clock_5.png"
    clock_6 = folder + "clock/clock_6.png"
    clock_7 = folder + "clock/clock_7.png"
    clock_8 = folder + "clock/clock_8.png"


class Label:
    def __init__(self, name: str, x: int, y: int, w: int, h: int, image_name: str, angle: int = 90, layer: int = 0) -> None:
        self._id: int = get_unique_id()
        self._name = name
        self._x = x
        self._y = y
        self._width = w
        self._height = h
        self._image_name = image_name
        self._image = pygame.image.load(self.image_name)
        self._layer = layer
        self._angle = angle
        self.angle = self.angle

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    @property
    def id(self):
        return self._id

    def _set_new_unick_id(self):
        self._id = get_unique_id()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, n):
        self._x = n

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, n):
        self._y = n

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, n):
        self._width = n

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, n):
        self._height = n

    @property
    def image_name(self):
        return self._image_name

    @image_name.setter
    def image_name(self, n):
        self._image_name = n

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, n):
        self._image = n

    def update_image(self):
        self.image = pygame.load(self.image_name)

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, n):
        self._layer = n

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, n):
        self._angle = n % 360
        if self._angle < 0:
            self._angle += 360

    def move_direction(self, direction):
        x += math.cos(direction / (360 / (math.pi * 2)))
        y += math.sin(direction / (360 / (math.pi * 2)))

    def move_forward(self):
        x += math.cos(self.angle / (360 / (math.pi * 2)))
        y += math.sin(self.angle / (360 / (math.pi * 2)))

    def update(self):
        pass

    def draw(self, screen, camera):
        image = self.image
        image = pygame.transform.rotate(image, self.angle - 90)
        image = pygame.transform.scale(
            image, (self.width, self.height))
        screen.blit(image, (self.x - self.width // 2,
                            settings.height - self.y - self.height // 2))


class Clock(Label):
    def __init__(self, m) -> None:
        super().__init__("Clock", 0, 0, 100, 100, ui_images.clock_0)
        self.images = list(map(lambda m: pygame.image.load(m), [ui_images.clock_0, ui_images.clock_1, ui_images.clock_2,
                                                                ui_images.clock_3, ui_images.clock_4, ui_images.clock_5,
                                                                ui_images.clock_6, ui_images.clock_7, ui_images.clock_8]))
        self.timer = 0
        self.map = m

    def update(self):
        self.x = self.width / 2 + 5
        self.y = settings.height - self.height / 2 - 5
        fps = settings.fps
        self.timer += 30 / fps
        if self.timer > 100:
            self.timer = 0
            self.map.step_update()
        self.image = selection(self.images, self.timer / 100)
