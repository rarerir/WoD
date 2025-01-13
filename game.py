import sys
import pygame as pg
from pygame import Clock
from math import floor
import pickle
import random


def calculate_move_vector(old_xy, speed, angle_in_degrees):
    move_vec = pg.math.Vector2()
    move_vec.from_polar((speed, angle_in_degrees))
    return old_xy + move_vec


class Board:
    # Создание поля
    def __init__(self, canvas, mapn, cell_size=30):
        self.load(mapn)
        self.canvas = canvas
        self.colors = ["black", "brown", "blue"]
        self.cell_size = cell_size
        self.left = (screenw - self.x * cell_size) / 2
        self.top = (screenh - self.y * cell_size) / 2
        self.drag = 0.8
        if self.left < 0:
            self.cell_size = floor(screenw / self.x)
            self.left = (screenw - self.x * self.cell_size) / 2
        if self.top < 0:
            if self.cell_size > floor(screenh / self.y):
                self.cell_size = floor(screenh / self.y)
            self.top = (screenh - self.y * self.cell_size) / 2
        self.left = (screenw - self.x * self.cell_size) / 2
        self.spawn()

    def render(self):
        for i in range(int(self.y)):
            for j in range(int(self.x)):
                eq = (j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size, self.cell_size)
                pg.draw.rect(self.canvas, self.colors[self.board[i][j]], eq)

    def load(self, mapnm):
        try:
            with(open(f'maps/{mapnm}.wmap', "rb")) as f:
                mapstr = pickle.load(f)
        except FileNotFoundError:
            print(f"Карта {mapnm} не найдена")
            sys.exit()
        self.x, self.y = mapstr.pop(-1)
        self.board = mapstr

    def spawn(self):
        spawn = (random.randrange(1, self.x + 1), random.randrange(1, self.y + 1))
        self.tank1 = Tank((450, 450), 1, 1, 1, self.drag, all_sprites)


class Tank(pg.sprite.Sprite):
    def __init__(self, spawn, speed, angspeed, hp, drag, *group):
        super().__init__(*group)
        # Програмные
        self.original_image = pg.image.load('sprites/крутой так.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=spawn)
        self.pos = spawn
        # Игровые
        self.hp = hp
        self.angle = 0
        self.angspeed = angspeed * 0.1
        self.speed = speed
        self.drag = drag
        # Управление
        self.da = 0
        self.dx = 0
        self.dy = 0

    def update(self, keys, isd):
        if isd:
            if keys[pg.K_UP]:
                self.pos = calculate_move_vector(self.pos, -self.speed, -self.angle + 90)
                self.rect.center = round(self.pos[0]), round(self.pos[1])
            if keys[pg.K_DOWN]:
                self.pos = calculate_move_vector(self.pos, self.speed, -self.angle + 90)
                self.rect.center = round(self.pos[0]), round(self.pos[1])
            if keys[pg.K_LEFT]:
                self.da = self.angspeed * dt
            if keys[pg.K_RIGHT]:
                self.da = -self.angspeed * dt
        if not (keys[pg.K_UP] or keys[pg.K_DOWN]):
            self.dx *= self.drag * dt
            self.dy *= self.drag * dt

        # Ограничения на скорость
        if abs(self.dx) < 0.01:
            self.dx = 0
        if abs(self.dy) < 0.01:
            self.dy = 0
        if abs(self.dy) > 100:
            self.dy = 100
        if abs(self.dy) > 100:
            self.dy = 100

        self.collisions()
        self.move()

    def collisions(self):
        if pg.sprite.spritecollideany(self, horizontal_borders):
            if self.dy < 0:
                self.dy = -self.dy + 1
            elif self.dy >= 0:
                self.dy = -self.dy - 1
        if pg.sprite.spritecollideany(self, vertical_borders):
            if self.dx < 0:
                self.dx = -self.dx + 1
            elif self.dx >= 0:
                self.dx = -self.dx - 1
        if self.hp < 0:
            self.kill()


    def move(self):
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.angle += self.da
        self.da = 0


class Border(pg.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pg.Surface([1, y2 - y1])
            self.rect = pg.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pg.Surface([x2 - x1, 1])
            self.rect = pg.Rect(x1, y1, x2 - x1, 1)


if __name__ == "__main__":
    pg.init()
    # Разрешение
    info = pg.display.Info()
    screenw = info.current_w
    screenh = info.current_h
    size = (screenw, screenh)
    screen = pg.display.set_mode(size)

    all_sprites = pg.sprite.Group()
    vertical_borders, horizontal_borders = pg.sprite.Group(), pg.sprite.Group()
    tanks = pg.sprite.Group()
    screen.fill((0, 0, 0))

    Border(5, 5, screenw - 5, 5)
    Border(5, screenh - 5, screenw - 5, screenh - 5)
    Border(5, 5, 5, screenh - 5)
    Border(screenw - 5, 5, screenw - 5, screenh - 5)

    running = True
    # Фпс
    v = 144
    clock = Clock()
    dt = clock.tick(v)

    board = Board(screen, "newmap")
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] in keys or keys[pg.K_DOWN] in keys or keys[pg.K_LEFT] in keys or keys[
            pg.K_RIGHT] in keys:
            all_sprites.update(keys, True)
        screen.fill((0, 0, 0))
        board.render()
        all_sprites.draw(screen)
        pg.display.flip()
        dt = clock.tick(v)
