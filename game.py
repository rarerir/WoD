import sys
import pygame as pg
from pygame.time import Clock
from math import floor
import math
from pygame import Vector2
import pickle
import random
import os


# Вектор движения
def calculate_move_vect(speed, angle_in_degrees):
    move_vec = Vector2()
    move_vec.from_polar((speed, angle_in_degrees))
    return move_vec


# Пересечение отрезков
def intersection(start1, end1, start2, end2):
    dir1 = end1 - start1
    dir2 = end2 - start2

    a1 = -dir1.y
    b1 = dir1.x
    d1 = -(a1 * start1.x + b1 * start1.y)

    a2 = -dir2.y
    b2 = dir2.x
    d2 = -(a2 * start2.x + b2 * start2.y)

    seg1_line2_start = a2 * start1.x + b2 * start1.y + d2
    seg1_line2_end = a2 * end1.x + b2 * end1.y + d2

    seg2_line1_start = a1 * start2.x + b1 * start2.y + d1
    seg2_line1_end = a1 * end2.x + b1 * end2.y + d1
    if seg1_line2_start * seg1_line2_end > 0 or seg2_line1_start * seg2_line1_end > 0:
        return False

    startend = seg1_line2_start - seg1_line2_end
    # Точка пересечения
    if startend == 0:
        u = 0
    else:
        u = seg1_line2_start / startend

    out_intersection = start1 + (dir1 * u)
    return out_intersection


def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image.set_colorkey(colorkey)
    return image


class Board:
    # Создание поля
    def __init__(self, mapn, cell_size=100):
        self.board = self.load(mapn)
        self.types = [0, 1, 2, 3]
        self.cell_size = cell_size
        self.board_width = self.x * self.cell_size
        self.board_height = self.y * self.cell_size
        self.power_couter = 0
        cells_colideable_b.empty()
        cells_colideable_t.empty()

        global screenw, screenh
        screenw = self.board_width
        screenh = self.board_height

        self.spawnable = [
            (y, x) for y in range(len(self.board))
            for x in range(len(self.board[y]))
            if self.board[y][x] == 0
        ]
        for i in range(int(self.y)):
            for j in range(int(self.x)):
                eq = (j * self.cell_size, i * self.cell_size)
                self.board[i][j] = Cell(eq, self.types[self.board[i][j]], cell_size=self.cell_size)

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == 0:
                    print(y, x)
        # Спавн игроков
        self.spawn_tanks()

    def load(self, mapnm):
        try:
            with(open(f'maps/{mapnm}.wmap', "rb")) as f:
                mapstr = pickle.load(f)
        except FileNotFoundError:
            print(f"Карта {mapnm} не найдена")
            sys.exit()
        self.x, self.y = mapstr.pop(-1)
        return mapstr

    def spawn_tanks(self):
        global tanks
        spawn = random.choice(self.spawnable)
        self.spawnable.remove(spawn)
        spawn1 = random.choice(self.spawnable)
        tank1_position = (
            (spawn[1] * self.cell_size) + (self.cell_size / 2),
            (spawn[0] * self.cell_size) + (self.cell_size / 2)
        )

        tank2_position = (
            (spawn1[1] * self.cell_size) + (self.cell_size / 2),
            (spawn1[0] * self.cell_size) + (self.cell_size / 2)
        )
        tank1 = Tank(tank1_position, 0.5, 3, 2, image="танчик2.png", id=1)
        tank2 = Tank(tank2_position, 0.5, 3, 2, key_forward=pg.K_w,
                     key_backward=pg.K_s, key_left=pg.K_a, key_right=pg.K_d, key_shoot=pg.K_e, image='танчик1.png', id=2)
        tanks.add(tank1)
        tanks.add(tank2)

    def spawn_powerups(self, dt):
        self.power_couter += 0.1 * dt
        if self.power_couter >= 1000:
            global power_ups
            spawn = random.choice(self.spawnable)
            powerup_position = (
                (spawn[1] * self.cell_size) + (self.cell_size / 2),
                (spawn[0] * self.cell_size) + (self.cell_size / 2)
            )
            Power_up(powerup_position, self.cell_size)
            self.power_couter = 0


class Cell(pg.sprite.Sprite):
    images = ['sprites/земля.jpg', 'sprites/кирпичи.png', 'sprites/вода.jpg', 'sprites/коробка.jpg']
    def __init__(self, eq, type=0, cell_size=30):
        super().__init__(all_sprites, cells)
        self.type = type
        self.cell_size = cell_size
        self.image = pg.image.load(f'{self.images[self.type]}')
        self.image = pg.transform.scale(self.image, (cell_size, cell_size))
        self.rect = self.image.get_rect(x=eq[0], y=eq[1])
        self.mask = pg.mask.from_surface(self.image)
        if self.type != 0:
            if self.type != 2:
                cells_colideable_b.add(self)
            cells_colideable_t.add(self)

    def reinit(self):
        cells_colideable_t.remove(self)
        cells_colideable_b.remove(self)
        self.image = pg.image.load(f'{self.images[self.type]}')
        self.image = pg.transform.scale(self.image, (self.cell_size, self.cell_size))

    def get_sides(self):
        return (Vector2(self.rect.topleft), Vector2(self.rect.bottomleft), Vector2(self.rect.topright),
                Vector2(self.rect.bottomright))

    def break_box(self):
        self.type = 0
        self.reinit()


class Power_up(pg.sprite.Sprite):
    abilities = {0:("rocket", "rocket.jpg"), 1:("bomb", "бомба.png"), 2:("bullet", "миниган.jpg"), 3:("C4", "c4.png")}
    def __init__(self, spawn, cell_size):
        super().__init__(all_sprites, power_ups)
        self.type = random.choice((0, 1, 2, 3))
        self.image = pg.image.load(f'sprites\\{self.abilities.get(self.type)[1]}')
        self.image = pg.transform.scale(self.image, (cell_size // 2, cell_size // 2))
        self.type = self.abilities.get(self.type)[0]
        self.rect = self.image.get_rect(x=spawn[0], y=spawn[1])
        self.pos = spawn

    def collect(self):
        return self.type


class Tank(pg.sprite.Sprite):
    types = {'shell': (5), 'bomb': (1), 'bullet': (100), 'rocket': (1), 'C4': (3)}
    def __init__(self, spawn, speed, angspeed, hp, size=(50, 50), key_forward=pg.K_UP,
                 key_backward=pg.K_DOWN, key_left=pg.K_LEFT, key_right=pg.K_RIGHT, key_shoot=pg.K_SPACE,
                 image='крутой так.png', id=1):
        super().__init__(all_sprites, tanks)
        # Игровые
        self.type = "C4"
        self.maxammo = self.types.get(self.type)
        self.currentammo = self.maxammo
        self.hp = hp
        self.id = id
        self.angle = 0
        self.angspeed = angspeed * 0.1
        self.speed = speed
        self.size = size
        self.original_image = pg.image.load(f'sprites/{image}')
        if self.type == 'bullet':
            self.shoot_sound = pg.mixer.Sound("sounds/minigun.mp3")
        else:
            self.shoot_sound = pg.mixer.Sound("sounds/выстрел.mp3")
        # Програмные
        self.original_image = pg.transform.scale(self.original_image, size)
        self.image = pg.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(center=spawn)
        self.mask = pg.mask.from_surface(self.image)
        self.pos = spawn
        # Управление
        self.key_forward = key_forward
        self.key_backward = key_backward
        self.key_left = key_left
        self.key_right = key_right
        self.key_shoot = key_shoot
        self.dx = 0
        self.dy = 0
        self.movement_enabled = True
        self.issound = False

    def reinit(self, type):
        self.maxammo = self.types.get(type)
        self.currentammo = self.maxammo
        self.type = type
        if self.type == 'bullet':
            self.shoot_sound = pg.mixer.Sound("sounds/minigun.mp3")
        else:
            self.shoot_sound.stop()
            self.issound = False
            self.shoot_sound = pg.mixer.Sound("sounds/выстрел.mp3")
        # Програмные
        # self.original_image = pg.transform.scale(self.original_image, size)
        # self.image = pg.transform.scale(self.original_image, size)
        # self.rect = self.image.get_rect(center=spawn)
        # self.mask = pg.mask.from_surface(self.image)

    def update(self, keys, dt):
        if self.movement_enabled:
            fps = self.speed * dt
            angfps = int(self.angspeed * dt)
            if keys[0][self.key_forward]:
                self.dx, self.dy = calculate_move_vect(-fps, -self.angle + 90)
            elif keys[0][self.key_backward]:
                self.dx, self.dy = calculate_move_vect(fps, -self.angle + 90)
            if keys[0][self.key_left]:
                self.angle += angfps
            elif keys[0][self.key_right]:
                self.angle -= angfps
        if self.type == 'bullet':
            if keys[0][self.key_shoot]:
                if self.currentammo > 0:
                    self.currentammo -= 1
                    self.shoot(dt)
                    if not self.issound:
                        self.shoot_sound.play(-1)
                        self.issound = True
                else:
                    self.reinit('shell')
                    if self.issound:
                        self.shoot_sound.stop()
                        self.issound = False
            else:
                if self.issound:
                    self.shoot_sound.stop()
                    self.issound = False
        else:
            for event in keys[1]:
                if event.type == pg.KEYDOWN and event.dict.get("key") == self.key_shoot:
                    if self.currentammo <= 0:
                        if self.type != 'shell':
                            if self.type == 'rocket':
                                self.movement_enabled = True
                            self.reinit('shell')
                    else:
                        self.currentammo -= 1
                        self.shoot(dt)
                        if self.type == 'rocket':
                            self.movement_enabled = False

        self.collisions()
        self.move()
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pg.mask.from_surface(self.image)

    def collisions(self):
        self.check_boolets()
        self.check_boundaries()
        self.check_cells()
        self.check_powerups()

    def check_boolets(self):
        for boolet in boolets:
            if pg.sprite.collide_mask(self, boolet):
                self.hp -= 1
                boolet.explode()

        if self.hp <= 0:
            self.explode()

    def check_boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenw:
            self.rect.right = screenw
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screenh:
            self.rect.bottom = screenh

    def check_cells(self):
        collided_cells = pg.sprite.spritecollide(self, cells_colideable_t, dokill=False)
        if collided_cells:
            for collided_cell in collided_cells:
                topleft, bottomleft, topright, bottomright = collided_cell.get_sides()
                linestart_l = Vector2(floor(self.rect.center[0] - self.dx + self.rect.left), floor(self.rect.center[1] - self.dy))

                linestart_r = Vector2(floor(self.rect.center[0] - self.dx - self.rect.right), floor(self.rect.center[1] - self.dy))
                # Я гений
                linestart_t = Vector2(floor(self.rect.center[0] - self.dx), floor(self.rect.center[1] - self.dy + self.rect.top))

                linestart_b = Vector2(floor(self.rect.center[0] - self.dx), floor(self.rect.center[1] - self.dy - self.rect.bottom))

                lineend = Vector2(self.rect.center[0], self.rect.center[1])
                # Верх
                if intersection(topleft, topright, linestart_t, lineend):
                    self.rect.bottom = collided_cell.rect.top
                # Низ
                if intersection(bottomleft, bottomright, linestart_b, lineend):
                    self.rect.top = collided_cell.rect.bottom
                # Лево
                if intersection(topleft, bottomleft, linestart_l, lineend):
                    self.rect.right = collided_cell.rect.left
                # Право
                if intersection(topright, bottomright, linestart_r, lineend):
                    self.rect.left = collided_cell.rect.right

    def check_powerups(self):
        collided_powerup = pg.sprite.spritecollideany(self, power_ups)
        if collided_powerup:
            type = collided_powerup.collect()
            collided_powerup.kill()
            self.reinit(type)

    def shoot(self, dt):
        shoot_channel = pg.mixer.Channel(1)
        if self.type != "bullet":
            shoot_channel.play(self.shoot_sound)
        spawn_position = (
             self.rect.centerx + calculate_move_vect(-self.size[1], -self.angle + 90)[0],
            self.rect.centery + calculate_move_vect(-self.size[1], -self.angle + 90)[1]
        )
        Boolet(self, self.speed * 1.3, self.angle, spawn_position, dt, self.key_left, self.key_right, self.key_shoot, type=self.type)

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.dx = 0
        self.dy = 0
        self.angle = self.angle % 360

    def explode(self):
        Explosion(self, self.rect.center, 100)


class Boolet(pg.sprite.Sprite):
    types = {'shell': (3, 1.3, 15), 'bomb': (100, 1.1, 30), 'bullet': (1, 1.8, 5), 'rocket': (10, 1, 40), 'C4': (1, 1, 10)}
    original_image = pg.image.load('sprites/bullet.png')
    def __init__(self, tank, speed, angle, center, dt, left, right, shoot, type='shell'):
        super().__init__(all_sprites, boolets)
        # Игровые
        self.radius = self.types.get(type)[2]
        self.speed = speed * self.types.get(type)[1]
        self.angle = angle
        self.hp = self.types.get(type)[0]
        self.type = type
        self.left = left
        self.right = right
        self.shoot = shoot

        # Спавн
        self.tank = tank
        vector = calculate_move_vect(-self.speed * dt, angle)
        x, y = vector + center
        self.dy, self.dx = vector

        # Картинка
        self.original_image = pg.transform.scale(self.original_image, (self.radius, self.radius))
        self.image = self.original_image
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect(center=(x, y))
        if self.check_cells(kill=True):
            self.explode()

    def update(self, events, dt):
        self.collisions()
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.type == 'rocket':
            angfps = int(dt)
            if events[0][self.left]:
                self.angle += angfps * 0.5
            elif events[0][self.right]:
                self.angle -= angfps * 0.5
            self.dx, self.dy = calculate_move_vect(-self.speed * dt, -self.angle + 90)
            self.image = pg.transform.rotate(self.original_image, self.angle + 90)
            for event in events[1]:
                if event.type == pg.KEYDOWN and event.dict.get("key") == self.shoot:
                    self.explode()
        else:
            self.angle = self.angle_hand()
            self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        if self.type == 'bomb':
            for event in events[1]:
                if event.type == pg.KEYDOWN and event.dict.get("key") == self.shoot:
                    self.explode()
        if self.hp <= 0:
            self.explode()
        self.rect = self.image.get_rect(center=self.rect.center)

    def angle_hand(self):
        angle = math.degrees(math.atan2(self.dx, self.dy))
        return angle % 360

    def collisions(self):
        if self.type != 'bullet':
            self.check_boolets()
        self.check_cells()
        self.check_boundaries()

    def check_boolets(self):
        bulcol = pg.sprite.spritecollide(self, boolets, False)
        if len(bulcol) > 1:
            for boolet in bulcol:
                boolet.hp -= 5

    def check_cells(self, kill=False):
        collided_cell = pg.sprite.spritecollideany(self, cells_colideable_b)
        if collided_cell:
            if self.type != 'C4':
                topleft, bottomleft, topright, bottomright = collided_cell.get_sides()
                linestart_l = Vector2(floor(self.rect.center[0] - self.dx + self.rect.left),
                                      floor(self.rect.center[1] - self.dy))

                linestart_r = Vector2(floor(self.rect.center[0] - self.dx - self.rect.right),
                                      floor(self.rect.center[1] - self.dy))
                linestart_t = Vector2(floor(self.rect.center[0] - self.dx),
                                      floor(self.rect.center[1] - self.dy + self.rect.top))

                linestart_b = Vector2(floor(self.rect.center[0] - self.dx),
                                      floor(self.rect.center[1] - self.dy - self.rect.bottom))

                lineend = Vector2(self.rect.center[0], self.rect.center[1])
                # Верх
                if intersection(topleft, topright, linestart_t, lineend):
                    self.dy = -self.dy
                    self.rect.top = collided_cell.rect.top - self.rect.height
                    if collided_cell.type == 3:
                        collided_cell.break_box()
                # Низ
                if intersection(bottomleft, bottomright, linestart_b, lineend):
                    self.dy = -self.dy
                    self.rect.bottom = collided_cell.rect.bottom + self.rect.height
                    if collided_cell.type == 3:
                        collided_cell.break_box()
                # Лево
                if intersection(topleft, bottomleft, linestart_l, lineend):
                    self.dx = -self.dx
                    self.rect.left = collided_cell.rect.left - self.rect.width
                    if collided_cell.type == 3: # Это не повтор, так надо или пули будут пролетать сквозь коробки
                        collided_cell.break_box()
                # Право
                if intersection(topright, bottomright, linestart_r, lineend):
                    self.dx = -self.dx
                    self.rect.right = collided_cell.rect.right + self.rect.width
                    if collided_cell.type == 3:
                        collided_cell.break_box()
                if kill and collided_cell.type == 3:
                    collided_cell.break_box()
            else:
                collided_cell.break_box()
                self.explode()
            return True

    def check_boundaries(self):
        if self.rect.bottom > screenh or self.rect.top < 0:
            self.dy = -self.dy
            self.angle = -self.angle + 180
            self.hp -= 1
        if self.rect.left < 0 or self.rect.right > screenw:
            self.dx = -self.dx
            self.angle = -self.angle % 360
            self.hp -= 1

    def explode(self):
        if self.type == 'shell' and self.tank.type == 'shell':
            self.tank.currentammo += 1
        if self.type != 'bullet':
            explosion_channel = pg.mixer.Channel(2)
            explosion_sound = pg.mixer.Sound("sounds/explosion.mp3")
            explosion_channel.play(explosion_sound)
            if self.type == 'rocket':
                self.tank.movement_enabled = True
            Explosion(self, self.rect.center, 100, self.type, angle=self.angle)
            Explosion(self, self.rect.center, 100, self.type, angle=self.angle)
        else:
            self.kill()


class Explosion(pg.sprite.Sprite):
    image = pg.image.load('sprites/explosion.jpg')
    image = pg.transform.scale(image, (10, 10))

    def __init__(self, thing, center, power, type="normal", duration=100, angle=False):
        super().__init__(all_sprites, explosions)
        self.power = power // duration
        self.rect = self.image.get_rect(center=center)
        self.angle = angle
        self.thing = thing
        self.center = center
        self.dispersion = 0
        self.type = type
        self.duration = duration
        self.c1 = 0
        if self.type == 'bomb':
            self.c1 = -40
        self.thing.kill()

    def update(self, events, dt):
        self.dispersion += self.power
        self.duration -= 1
        if self.duration == 0:
            self.kill()
        self.image = pg.transform.scale(self.image, (self.dispersion, self.dispersion))
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.type == "bomb" or self.type == "tank" or self.type == 'rocket':
            while self.c1 < 30:
                self.c1 += 1
                if self.type == "bomb":
                    shard = Shard(self.center[0], self.center[1], isdeadly=True)
                elif self.type == "rocket":
                    shard = Shard(self.center[0], self.center[1], isdeadly=True, angle=self.angle)
                else:
                    shard = Shard(self.center[0], self.center[1], color='white')
                all_sprites.add(shard)

class Shard(pg.sprite.Sprite):
    def __init__(self, x, y, isdeadly=False, color='red', angle=None):
        self.size = 7
        super(Shard, self).__init__()
        self.image = pg.Surface([self.size, self.size])
        self.pt1 = random.randint(0, self.size)
        self.pt2 = random.randint(0, self.size)
        self.image.set_colorkey("black")
        pg.draw.polygon(self.image, color, ((0, 0), (self.size, self.pt1), (self.pt2, self.size)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity = 1
        if angle:
            a, b = abs(int(angle + 200)), abs(int(angle + 160))
            if a > b:
                self.angle = math.radians(random.randint(b, a))
            else:
                self.angle = math.radians(random.randint(a, b))
        else:
            self.angle = math.radians(random.randint(0, 360))

        self.dx = self.velocity * math.sin(self.angle)
        self.dy = self.velocity * math.cos(self.angle)

        self.isdeadly = isdeadly
        self.hp = 100

    def update(self, events, dt):
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt
        self.collisions()

    def collisions(self):
        self.check_cells()
        self.check_boundaries()
        if self.hp < 0:
            self.kill()
        if self.isdeadly:
            self.check_tanks()

    def check_cells(self):
        collided_cell = pg.sprite.spritecollideany(self, cells_colideable_b)
        if collided_cell:
            self.dx = 0
            self.dy = 0
            self.hp -= 1

    def check_boundaries(self):
        if self.rect.bottom > screenh or self.rect.top < 0:
            self.dx = 0
            self.dy = 0
            self.hp -= 1
        if self.rect.left < 0 or self.rect.right > screenw:
            self.dx = 0
            self.dy = 0
            self.hp -= 1

    def check_tanks(self):
        colided = pg.sprite.spritecollideany(self, tanks)
        if colided:
            colided.hp -= 1
            self.kill()


class Game:
    def __init__(self, size):
        global cells_colideable_t, cells_colideable_b, tanks, boolets, explosions, all_sprites, power_ups, cells
        pg.init()
        # Группы спрайтов
        all_sprites = pg.sprite.Group()
        cells, cells_colideable_t, cells_colideable_b = pg.sprite.Group(), pg.sprite.Group(), pg.sprite.Group()
        power_ups = pg.sprite.Group()
        tanks = pg.sprite.Group()
        boolets = pg.sprite.Group()
        explosions = pg.sprite.Group()
        # Разрешение
        self.size = size
        self.gscreen = pg.display.set_mode(self.size)
        self.gscreen.fill((0, 0, 0))
        # Экран конца
        self.fade_in = True
        self.a = 255
        self.fade_speed = 2
        self.font = pg.font.Font(None, 74)
        # Победы
        self.wins_player1 = 0
        self.wins_player2 = 0
        self.playerw1 = False
        self.playerw2 = False
        # Фпс
        self.v = 144
        self.clock = Clock()
        self.paused = False

        self.board = self.load_random_board()

    def load_random_board(self):
        map_files = [f for f in os.listdir('maps') if f.endswith('.wmap')]

        if not map_files:
            print("Нет доступных карт для загрузки.")
            sys.exit()

        random_map_file = random.choice(map_files)
        print(f"Загрузка карты: {random_map_file}")

        board = Board(random_map_file[:-5])
        return board

    def draw_pause_screen(self):
        all_sprites.draw(self.gscreen)

        font = pg.font.Font(None, 74)
        text = font.render("Пауза", True, (200, 200, 200))
        text_rect = text.get_rect(center=(screenw // 2, screenh // 2))
        self.gscreen.blit(text, text_rect)

    def draw_win_counter(self):
        font = pg.font.Font(None, 36)
        win_text = f"Игрок 1 : {self.wins_player1}   Игрок 2 : {self.wins_player2}"
        text = font.render(win_text, True, (255, 100, 100))
        self.gscreen.blit(text, (10, 10))

    def draw_game_over_screen(self):
        self.gscreen.fill((0, 0, 0))
        font = pg.font.Font(None, 100)
        zfont = pg.font.Font(None, 40)
        if tanks.sprites()[0].id == 1:
            text = font.render("Игрок 1 победил", True, (0, 250, 0))
            self.playerw1 = True
        if tanks.sprites()[0].id == 2:
            text = font.render("Игрок 2 победил", True, (0, 250, 0))
            self.playerw2 = True
        text_rect = text.get_rect(center=(screenw // 2, screenh - 650))
        self.gscreen.blit(text, text_rect)

        restart_text = zfont.render("Нажмите R для перезапуска", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(screenw // 2, screenh - 300))

        restart_text.set_alpha(self.a)
        self.gscreen.blit(restart_text, restart_rect)

        pg.display.flip()

    def update_fade(self):
        if self.fade_in:
            self.a -= self.fade_speed
            if self.a <= 0:
                self.fade_in = False
        else:
            self.a += self.fade_speed
            if self.a >= 255:
                self.fade_in = True

    def reset_game(self):
        global all_sprites, tanks, boolets, explosions
        all_sprites.empty()
        tanks.empty()
        boolets.empty()
        explosions.empty()
        pg.mixer.stop()
        if self.playerw1:
            self.wins_player1 += 1
            self.playerw1 = False
        elif self.playerw2:
            self.wins_player2 += 1
            self.playerw2 = False
        self.board = Board("rar")

    def mainloop(self):
        running = True
        while running:
            dt = self.clock.tick(self.v)
            self.gscreen.fill((0, 0, 0))
            # Эвенты
            events = pg.event.get()
            keys = pg.key.get_pressed()
            for event in events:
                if event.type == pg.QUIT:
                    return False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.paused = not self.paused
                    if event.key == pg.K_r and len(tanks) < 2:
                        self.reset_game()

            if self.paused:
                self.draw_pause_screen()
            elif len(tanks) < 2:
                self.draw_game_over_screen()
                self.update_fade()
            else:
                self.gscreen.fill((0, 0, 0))
                # Обновление спрайтов
                all_sprites.update((keys, events), dt)
                all_sprites.draw(self.gscreen)
                self.board.spawn_powerups(dt)
                self.draw_win_counter()
            pg.display.flip()


if __name__ == "__main__":
    game = Game((1000, 1000))
    game.mainloop()
