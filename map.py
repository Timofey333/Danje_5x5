import pygame
from game_objects import *
from base import RoomBase
from camera import Camera
import settings
from log import Log
from random import randint, choice
import rooms
import copy
import ui


class floor_palette:
    blue = ["#858585", "#969696", "#adadad",
            "#373d75", "#684596", "#459196",
            "#545875", "#796396", "#6a9194",
            "#676978", "#877999", "#7b9294"]
    slime = ["#858585", "#969696", "#adadad",
             "#718c6f", "#5b7f58", "#658f73"]
    stone = ["#595959", "#595959", "#7f7f7f",
             "#8f8f8f", "#9e9e9e", "#7b7b85",
             "#777282", "#777891", "#6b6b75"]
    gold = ["#737373", "#666666", "#8c8c8c",
            "#aba97b", "#a6a34e", "#c1c781",
            "#c78181", "#967474", "#f5fca4"]

    palletes = {"blue": blue, "slime": slime, "stone": stone,
                "gold": gold}

    def get(name):
        return floor_palette.palletes.get(name, floor_palette.blue)


class Room:
    def __init__(self, plan) -> None:
        width, height = plan["width"], plan["height"]
        self._plan = plan
        self.color_plan = [[choice(floor_palette.get(plan["palette"])) for _ in range(width)]
                           for _ in range(height)]
        self._id = get_unique_id()
        self.field = [[[] for _ in range(width)] for _ in range(height)]
        self._width, self._height = width, height

    @property
    def id(self):
        return self._id

    @property
    def plan(self):
        return self._plan

    def plan_init(self, map):
        plan = self._plan
        for t, positions in plan.items():
            if type(positions) != list:
                continue
            for pos in positions:
                x, y = pos
                sx, sy = self.tile_to_screen_pos(x, y)
                if t == "W":
                    self.add(x, y, Wall(sx, sy))
                elif t in "0123456789":
                    if type(self.plan[t]) == Door:
                        continue
                    if randint(1, 3) == 1 or plan["is_spawn"] or map.base.len_rooms <= 3:
                        door = Door(
                            map, *self.tile_to_screen_pos(x, y), images.random_door(), int(t), self.id, -1)
                        self.add(x, y, door)
                        self.plan[t] = door
                elif t == "S":
                    if randint(1, 3) <= 1:
                        continue
                    self.add(x, y, Slime(sx, sy))
                elif t == "s":
                    if randint(1, 3) <= 1:
                        continue
                    self.add(x, y, Spider(sx, sy))
                elif t == "n":
                    if randint(1, 3) <= 1:
                        continue
                    self.add(x, y, Net(sx, sy))
                elif t == "m":
                    if randint(1, 3) <= 1:
                        continue
                    self.add(x, y, Money(sx, sy))
        for i in range(10):
            if str(i) not in plan:
                continue
            t = plan[str(i)]
            if type(t) == Door:
                t.init()
        # for end rooms
        if plan["is_end"]:
            for _ in range(0, 10):
                x, y = self.get_open_pos()
                r = randint(1, 100)
                t = None
                if r <= 70:
                    t = Wall
                elif r <= 90:
                    t = Slime
                else:
                    t = Money
                self.add(x, y, t(*self.tile_to_screen_pos(x, y)))
        # create flora
        for _ in range(randint(0, 5)):
            x, y = self.get_open_pos()
            self.add(x, y, Flora(*self.tile_to_screen_pos(x, y)))

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def get(self, x, y):
        return self.field[y][x]

    def obj_pos(self, obj) -> GameObject or None:
        for x in range(self.width):
            for y in range(self.height):
                for g in self.get(x, y):
                    if g == obj:
                        return x, y
        return None

    def add(self, x, y, obj):
        self.field[y][x].append(obj)

    def rem(self, x, y, obj):
        self.field[y][x].remove(obj)

    def get_open_pos(self):
        while True:
            x, y = randint(0, self.width - 1), randint(0, self.height - 1)
            if len(self.get(x, y)) == 0:
                return x, y

    def tile_to_screen_pos(self, x, y):
        nx = x * settings.tile - self.width / 2 * settings.tile + 0.5 * settings.tile
        ny = y * settings.tile - self.height / 2 * settings.tile + 0.5 * settings.tile
        return nx, ny

    def screen_to_tile_pos(self, x, y):
        nx = x / settings.tile + self.width / 2 - 0.5
        ny = y / settings.tile + self.height / 2 - 0.5
        return int(nx), int(ny)

    def draw(self, screen, camera: Camera):
        tile = settings.tile
        right_x = settings.width // 2 - camera.pos_x + 0 * tile - self.width / 2 * tile
        left_x = settings.width // 2 - camera.pos_x + \
            self.width * tile - self.width / 2 * tile
        right_y = settings.height // 2 + camera.pos_y - 0 * tile + self.height / 2 * tile
        left_y = settings.height // 2 + camera.pos_y - \
            self.height * tile + self.height / 2 * tile
        # draw_fon
        pygame.draw.rect(screen, "#858585", (right_x, left_y,
                         self.width * tile, self.height * tile))
        for y in range(self.height):
            for x in range(self.width):
                rx = settings.width / 2 - camera.pos_x + x * tile - self.width / 2 * tile
                ry = settings.height / 2 + camera.pos_y - \
                    y * tile + self.height / 2 * tile - tile
                pygame.draw.rect(
                    screen, self.color_plan[y][x], (rx, ry, tile, tile), 0, 0)
        # draw_lines
        for y in range(0, self.height + 1):
            ly = settings.height // 2 + camera.pos_y - y * tile + self.height / 2 * tile
            if ly == left_y or ly == right_y:
                b = 5
            else:
                b = 1
            pygame.draw.line(screen, (0, 0, 0), (right_x, ly), (left_x, ly), b)
        for x in range(0, self.width + 1):
            lx = settings.width // 2 - camera.pos_x + x * tile - self.width / 2 * tile
            if lx == left_x or lx == right_x:
                b = 5
            else:
                b = 1
            pygame.draw.line(screen, (0, 0, 0), (lx, right_y), (lx, left_y), b)
        # draw game objects
        game_objects = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                for game_object in self.get(x, y):
                    game_objects.append(game_object)
        for game_object in sorted(game_objects, key=lambda g: g.layer):
            game_object.draw(screen, camera)


class Map(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.base = RoomBase("base.bd")
        self._room = Room(copy.copy(rooms.spawn_room))
        self.base.add(self.room)
        self.room.plan_init(self)
        self.camera = Camera(self, 0, 0)
        self._log = Log()
        x, y = self.room.get_open_pos()
        self._player = Knight(*self.room.tile_to_screen_pos(x, y))
        self.room.add(x, y, self._player)
        self.net_table_image = pygame.transform.scale(
            pygame.image.load(images.net_table), (150, 150))
        self.ui = []
        timer = ui.Clock(self)
        self.ui.append(timer)

    @property
    def log(self):
        return self._log

    @property
    def room(self):
        return self._room

    @property
    def player(self):
        return self._player

    @room.setter
    def room(self, n):
        self._room = n

    def add_object(self, object: GameObject):
        self.objects.append(object)

    def set_camera(self, camera: Camera):
        self.camera = camera

    def draw(self, screen):
        self.room.draw(screen, self.camera)
        if self.player.is_in_net:
            screen.blit(self.net_table_image,
                        (settings.width / 2 - self.net_table_image.get_width() // 2, settings.height - 150))
        for l in sorted(self.ui, key=lambda l: l.layer, reverse=True):
            l.draw(screen, self.camera)

    def update(self):
        for l in self.ui:
            l.update()
        for x in range(self.room.width):
            for y in range(self.room.height):
                for g in self.room.get(x, y):
                    g.update()

    def step_update(self):
        update_objects = []
        for y in range(self.room.height):
            for x in range(self.room.width):
                for g in self.room.get(x, y):
                    update_objects.append(g)
        for g in update_objects:
            g.step_update(self.room)

    def create_room(self, door):
        if self.base.len_rooms <= settings.rooms:
            plan = copy.copy(rooms.find_room_with_door(
                rooms.GENERAL_ROOMS, door.door_number))
        else:
            plan = copy.copy(rooms.find_room_with_door(
                rooms.END_ROOMS, door.door_number))
        room = Room(plan)
        self.base.add(room)
        x, y = plan[str(door.door_number)][random.randint(
            0, len(plan[str(door.door_number)]) - 1)]
        door_2 = Door(self, *room.tile_to_screen_pos(x, y), door.image_name, door.door_number,
                      room.id, door.room_1_id, (door.x, door.y))
        door.door_2_pos = (door_2.x, door_2.y)
        room.plan[str(door.door_number)] = door_2
        room.add(x, y, door_2)
        room.plan_init(self)
        return room

    def set_room(self, room, door):
        self.room.rem(*self.player.get_pos(self.room), self.player)
        door_2 = room.plan[str(door.door_number)]
        if type(door_2) == list:
            print()
        x, y = room.screen_to_tile_pos(door_2.x, door_2.y)
        room.add(x, y, self.player)
        self.player.set_pos(*room.tile_to_screen_pos(x, y))
        self.room = room
        self.log.error(str(room.id))
