from email.mime import image
import math
import os
import pickle
import random
from turtle import forward

import pygame

import settings


class images:
    folder = "images/"
    field = folder + "5x5_field.png"
    wall = folder + "/walls/wall_0.png"
    knight = folder + "knight.png"
    money = folder + "money.png"
    net = folder + "net/net_0.png"
    net_table = folder + "net/net_1.png"

    thorn_1 = folder + "thorns/thorn_0.png"
    thorn_2 = folder + "thorns/thorn_1.png"
    thorn_3 = folder + "thorns/thorn_2.png"
    thorn_4 = folder + "thorns/thorn_3.png"
    thorn_5 = folder + "thorns/thorn_4.png"

    flora_folder = folder + "flora/"
    flora_0 = flora_folder + "plant_00.png"
    flora_1 = flora_folder + "plant_01.png"
    flora_2 = flora_folder + "plant_02.png"
    flora_3 = flora_folder + "plant_03.png"
    flora_4 = flora_folder + "plant_04.png"
    flora_5 = flora_folder + "plant_05.png"
    flora_6 = flora_folder + "plant_06.png"
    flora_7 = flora_folder + "plant_07.png"
    flora_8 = flora_folder + "plant_08.png"
    flora_9 = flora_folder + "plant_09.png"

    monsters_folder = folder + "monsters/"

    slime_0 = monsters_folder + "slime/slime_0.png"
    slime_1 = monsters_folder + "slime/slime_1.png"
    slime_2 = monsters_folder + "slime/slime_2.png"
    slime_3 = monsters_folder + "slime/slime_3.png"
    slime_4 = monsters_folder + "slime/slime_4.png"
    slime_5 = monsters_folder + "slime/slime_5.png"
    slime_6 = monsters_folder + "slime/slime_6.png"
    slime_7 = monsters_folder + "slime/slime_7.png"
    slime_8 = monsters_folder + "slime/slime_8.png"

    slime_caviar_0 = monsters_folder + "slime_caviar/slime_caviar_0.png"
    slime_caviar_1 = monsters_folder + "slime_caviar/slime_caviar_1.png"

    spider_0 = monsters_folder + "spider/spider_0.png"
    spider_1 = monsters_folder + "spider/spider_1.png"
    spider_2 = monsters_folder + "spider/spider_2.png"
    spider_3 = monsters_folder + "spider/spider_3.png"
    spider_4 = monsters_folder + "spider/spider_4.png"

    door_folder = "images/doors/"
    door_loop = door_folder + "door_loop.png"
    golden_door = door_folder + "door_01.png"
    door = door_folder + "door_02.png"
    liana_door = door_folder + "door_03.png"
    rotten_door = door_folder + "door_04.png"
    iron_window_door = door_folder + "door_05.png"
    # latch_iron_window_door = door_folder + "door_06.png"
    # open_latch_iron_window_door = door_folder + "door_07.png"
    # latch_door = door_folder + "door_08.png"
    # open_latch_door = door_folder + "door_09.png"
    net_door = door_folder + "door_10.png"
    slime_door = door_folder + "door_11.png"
    crystal_door = door_folder + "door_12.png"

    def random_door():
        return random.choice([images.door, images.golden_door, images.liana_door,
                              images.rotten_door, images.iron_window_door, images.net_door])


def get_unique_id():
    if os.path.exists("last_id.pickle"):
        last_id = -1
        with open("last_id.pickle", "rb") as f:
            last_id = pickle.load(f)
        last_id += 1
        with open("last_id.pickle", "wb") as f:
            pickle.dump(last_id, f)
        return last_id
    else:
        last_id = 0
        with open("last_id.pickle", "wb") as f:
            pickle.dump(last_id, f)
        return last_id


def _set_last_id(new_id):
    with open("last_id.pickle", "wb") as f:
        pickle.dump(new_id, f)


def lerp(a, b, t):
    if a > b:
        return a - b - (a - b) * t
    return a + (b - a) * t


def selection(l: list, t: float):
    return l[int(lerp(0, len(l) - 1, t))]


class GameObject:
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
        self._start_move_x, self._start_move_y = x, y
        self._target_x, self._target_y = x, y
        self._hp = 1

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
    def start_move_x(self):
        return self._start_move_x

    @start_move_x.setter
    def start_move_x(self, n):
        self._start_move_x = n

    @property
    def start_move_y(self):
        return self._start_move_y

    @start_move_y.setter
    def start_move_y(self, n):
        self._start_move_y = n

    @property
    def target_x(self):
        return self._target_x

    @target_x.setter
    def target_x(self, n):
        self._target_x = n

    @property
    def target_y(self):
        return self._target_y

    @target_y.setter
    def target_y(self, n):
        self._target_y = n

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
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, n):
        self._hp = n

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

    def damage(self, strong):
        pass

    def move(self, x, y):
        self.x += x
        self.y += y

    def get_pos(self, room):
        x, y = room.screen_to_tile_pos(self.target_x, self.target_y)
        if self in room.get(x, y):
            return x, y
        else:
            return room.obj_pos(self)

    def is_borders(self, room, x, y):
        if x < 0 or y < 0:
            return True
        if x >= room.width or y >= room.height:
            return True
        return False

    def collide_type(self, room, x, y, t, if_borders=[]) -> list:
        if self.is_borders(room, x, y):
            return if_borders
        a = []
        for g in room.get(x, y):
            if type(g) == t:
                a.append(g)
        return a

    def collide_types(self, room, x, y, ts, if_borders=[]) -> list:
        if self.is_borders(room, x, y):
            return if_borders
        a = []
        for g in room.get(x, y):
            if type(g) in ts:
                a.append(g)
        return a

    def move_tile(self, room, move_x, move_y) -> bool:
        x, y = self.get_pos(room)
        if self.is_borders(room, x + move_x, y + move_y):
            return False
        room.rem(x, y, self)
        self.start_move_x, self.start_move_y = room.tile_to_screen_pos(x, y)
        self.target_x, self.target_y = room.tile_to_screen_pos(
            x + move_x, y + move_y)
        room.add(x + move_x, y + move_y, self)
        return True

    def move_tile_with_out_collide_types(self, room, move_x, move_y, ts) -> bool:
        x, y = self.get_pos(room)
        if self.is_borders(room, x + move_x, y + move_y):
            return False
        if self.collide_types(room, x + move_x, y + move_y, ts):
            return False
        room.rem(x, y, self)
        self.start_move_x, self.start_move_y = room.tile_to_screen_pos(x, y)
        self.target_x, self.target_y = room.tile_to_screen_pos(x, y)
        room.add(x + move_x, y + move_y, self)
        return True

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.start_move_x = x
        self.start_move_y = y

    def rotate(self, a):
        self.angle += a

    def set_rotate(self, a):
        self.a = a

    def move_direction(self, direction):
        x += math.cos(direction / (360 / (math.pi * 2)))
        y += math.sin(direction / (360 / (math.pi * 2)))

    def move_forward(self):
        x += math.cos(self.angle / (360 / (math.pi * 2)))
        y += math.sin(self.angle / (360 / (math.pi * 2)))

    def update(self):
        if (self.x == self.target_x and self.y == self.target_y):
            return
        for _ in range(20):
            x, y = int(self.x), int(self.y)
            target_x, target_y = int(self.target_x), int(self.target_y)
            if x < target_x:
                self.move(1, 0)
            if x > target_x:
                self.move(-1, 0)
            if y < target_y:
                self.move(0, 1)
            if y > target_y:
                self.move(0, -1)

    def step_update(self, room):
        pass

    def draw(self, screen, camera):
        image = self.image
        image = pygame.transform.rotate(image, self.angle - 90)
        image = pygame.transform.scale(
            image, (settings.tile * self.width, settings.tile * self.height))
        screen.blit(image, (settings.width // 2 - camera.pos_x + self.x - settings.tile * self.width // 2,
                            settings.height // 2 + camera.pos_y - self.y - settings.tile * self.height // 2))


class Wall(GameObject):
    def __init__(self, x, y) -> None:
        super().__init__("wall", x, y, 1, 1, images.wall, layer=1)


class Door(GameObject):
    def __init__(self, map, x, y, image_name, door_number, room_1_id, room_2_id=-1, door_2_pos=(-1, -1)):
        super().__init__("door", x, y, 1, 1, image_name, layer=-2)
        self.map = map
        self._door_number = door_number
        self._room_1_id = room_1_id
        self._room_2_id = room_2_id
        self._door_2_pos = door_2_pos
        self._is_lighting = False
        self.lighting_image = pygame.image.load(images.door_loop)

    @property
    def door_number(self):
        return self._door_number

    @property
    def room_1_id(self):
        return self._room_1_id

    @property
    def room_2_id(self):
        return self._room_2_id

    @property
    def door_2_pos(self):
        return self._door_2_pos

    @door_2_pos.setter
    def door_2_pos(self, n):
        self._door_2_pos = n

    @property
    def is_lighting(self):
        return self._is_lighting

    @is_lighting.setter
    def is_lighting(self, n):
        self._is_lighting = n

    def init(self):
        self.was_init = True
        if self.room_2_id == -1:
            if random.randint(1, 3) == 1:
                room = self.map.create_room(self)
                self._room_2_id = room.id
            else:
                room = self.map.base.random()
                if str(self.door_number) not in room.plan.keys():
                    room = self.map.create_room(self)
                    self._room_2_id = room.id
                    return
                if type(room.plan[str(self.door_number)]) == Door:
                    room = self.map.create_room(self)
                    self._room_2_id = room.id
                    return
                self._room_2_id = room.id
                x, y = room.plan[str(self.door_number)][random.randint(
                    0, len(room.plan[str(self.door_number)]) - 1)]
                door_2 = Door(self.map, *room.tile_to_screen_pos(x, y), self.image_name,
                              self.door_number, self.room_1_id, room.id, (self.x, self.y))
                self.door_2_pos = door_2.x, door_2.y
                room.add(x, y, door_2)
                room.plan[str(self.door_number)] = door_2
                print("Link ", self.room_1_id, self.room_2_id)

    def draw(self, screen, camera):
        if self.is_lighting:
            image = self.image
            self.image = self.lighting_image
            super().draw(screen, camera)
            self.image = image
        return super().draw(screen, camera)

    def open_door(self, room):
        self.is_lighting = True
        if room.id == self.room_1_id:
            room_2 = self.map.base.id_get(self.room_2_id)
        else:
            room_2 = self.map.base.id_get(self.room_1_id)
        if room_2 is None:
            print(self.room_1_id, self.room_2_id)
        for g in room_2.get(*room_2.screen_to_tile_pos(*self.door_2_pos)):
            if type(g) == Door:
                g.is_lighting = True
        self.map.set_room(room_2, self)


class Net(GameObject):
    def __init__(self, x, y) -> None:
        super().__init__("Net", x, y, 1, 1, images.net, layer=-1)


class Money(GameObject):
    def __init__(self, x, y) -> None:
        super().__init__("Money", x, y, 1, 1, images.money, layer=-1)


class Knight(GameObject):
    def __init__(self, x, y) -> None:
        super().__init__("knight", x, y, 1, 1, images.knight, layer=1)
        self.hp = 10
        self.net_tab = "right"
        self._is_in_net = False
        self._money = 0

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, n):
        self._money = n

    def move_player(self, map, move_x, move_y):
        room = map.room
        x, y = self.get_pos(room)
        nx, ny = x + move_x, y + move_y
        if len(self.collide_types(room, nx, ny, COLLIDE_OBJECTS)) != 0:
            return
        if self.move_tile(room, move_x, move_y):
            map.step_update()
        m = self.collide_type(room, x + move_x, y + move_y, Money)
        if m:
            room.rem(x + move_x, y + move_y, m[0])
            self.money += 1
        net = self.collide_type(room, x + move_x, y + move_y, Net)
        if net:
            self._is_in_net = True

    @property
    def is_in_net(self):
        return self._is_in_net

    def damage(self, strong):
        self.hp -= strong

    def key_event(self, event, map):
        if event.type == pygame.KEYDOWN:
            room = map.room
            x, y = self.get_pos(room)
            net = self.collide_type(room, x, y, Net)
            if net:
                self._is_in_net = True
                if event.key == pygame.K_RIGHT and self.net_tab == "right":
                    self.net_tab = "left"
                elif event.key == pygame.K_LEFT and self.net_tab == "left":
                    self.net_tab = "right"
                else:
                    return
                if random.randint(1, 5) == 1:
                    room.rem(x, y, net[0])
                    self._is_in_net = False
                if random.randint(1, 5) == 1:
                    map.step_update()
                return
            if event.key == pygame.K_UP:
                self. move_player(map, 0, 1)
            if event.key == pygame.K_DOWN:
                self.move_player(map, 0, -1)
            if event.key == pygame.K_RIGHT:
                self.move_player(map, 1, 0)
            if event.key == pygame.K_LEFT:
                self.move_player(map, -1, 0)
            if event.key == pygame.K_KP_0:
                c = self.collide_type(room, *self.get_pos(room), Door)
                if c:
                    c[0].open_door(room)
            if event.key == pygame.K_t:
                map.step_update()

    def update_camera_pos(self, camera):
        camera.pos_x, camera.pos_y = self.x, self.y


class Slime(GameObject):
    def __init__(self, x, y):
        super().__init__("Slime", x, y, 1, 1, images.slime_0, layer=1)
        self.forward = self.random_forward()
        self.go_anim_images = list(map(lambda m: pygame.image.load(m), [images.slime_0, images.slime_1, images.slime_2,
                                                                        images.slime_3, images.slime_4, images.slime_5, images.slime_6,
                                                                        images.slime_7, images.slime_8]))

    def random_forward(self):
        return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def step_update(self, room):
        x, y = self.get_pos(room)
        c = self.collide_types(
            room, x + self.forward[0], y + self.forward[1], COLLIDE_OBJECTS, None)
        if c is None:
            self.forward = self.random_forward()
            return
        if Knight in list(map(lambda g: type(g), c)):
            # damage
            for g in c:
                if type(g) == Knight:
                    g.damage(1)
                    break
            self.forward = self.random_forward()
            return
        if len(c) != 0:
            self.forward = self.random_forward()
            return
        self.move_tile(room, *self.forward)

    def draw(self, screen, camera):
        sp = self.start_move_x + self.start_move_y
        p = max(abs(self.x + self.y - sp), 1)
        tp = max(abs(self.target_x + self.target_y - sp), 1)
        p, tp = (tp, p) if p > tp else (p, tp)
        f = ((p * (100 / tp)) / (tp * (100 / tp)))
        self.image = selection(self.go_anim_images, f)
        super().draw(screen, camera)


class Spider(GameObject):
    def __init__(self, x, y):
        super().__init__("Spider", x, y, 1, 1, images.slime_0, layer=1)
        self.forward = self.random_forward()
        self.go_anim_images = list(map(lambda m: pygame.image.load(m), [images.spider_0, images.spider_1, images.spider_2,
                                                                        images.spider_3, images.spider_4]))

    def random_forward(self):
        return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def step_update(self, room):
        x, y = self.get_pos(room)
        c = self.collide_types(
            room, x + self.forward[0], y + self.forward[1], COLLIDE_OBJECTS, None)
        if c is None:
            self.forward = self.random_forward()
            return
        if Knight in list(map(lambda g: type(g), c)):
            # damage
            for g in c:
                if type(g) == Knight:
                    g.damage(1)
                    break
            self.forward = self.random_forward()
            return
        if len(c) != 0:
            self.forward = self.random_forward()
            return
        self.move_tile(room, *self.forward)

    def draw(self, screen, camera):
        sp = self.start_move_x + self.start_move_y
        p = max(abs(self.x + self.y - sp), 1)
        tp = max(abs(self.target_x + self.target_y - sp), 1)
        p, tp = (tp, p) if p > tp else (p, tp)
        f = ((p * (100 / tp)) / (tp * (100 / tp)))
        self.image = selection(self.go_anim_images, f)
        super().draw(screen, camera)


class Flora(GameObject):
    def __init__(self, x, y, image_name=None) -> None:
        if image_name is None:
            image_name = random.choice([images.flora_0, images.flora_1,
                                        images.flora_2, images.flora_3, images.flora_4, images.flora_5,
                                        images.flora_6, images.flora_7, images.flora_8, images.flora_9])
        super().__init__("Flora", x, y, 1, 1, image_name, layer=-1)


WALLS = [Wall]
MONSTERS = [Slime, Spider]
COLLIDE_OBJECTS = [Knight] + WALLS + MONSTERS
