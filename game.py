import math
import pickle
import random
import sys
from math import floor

import pygame as pg
from pygame import Vector2
from pygame.time import Clock


class Board:
    # Создание поля
    def __init__(self, canvas, mapn, cell_size=30):
        self.load(mapn)
        self.canvas = canvas
        self.colors = ["black", "brown", "blue"]
        self.cell_size = cell_size
        self.left = (screenw - self.x * cell_size) / 2
        self.top = (screenh - self.y * cell_size) / 2
        self.drag = 0.7
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
                eq = (j * self.cell_size + self.left, i * self.cell_size + self.top, *([self.cell_size] * 2))
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
        print(mapstr)

    def spawn(self):
        spawn = (random.randrange(1, self.x + 1), random.randrange(1, self.y + 1))
        self.tank1 = Tank(spawn, 1, 1, self.drag, all_sprites)


class Tank(pg.sprite.Sprite):
    def __init__(self, spawn, speed, angspeed, drag, *group):
        super().__init__(*group)
        # Програмные
        self.original_image = pg.image.load('sprites/крутой так.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect = pg.Rect(self.rect.y, self.rect.x, self.rect.h, self.rect.w)
        # Игровые
        self.spawn = spawn
        self.angle = 0
        self.angspeed = angspeed
        self.speed = speed
        self.drag = drag
        print(self.spawn)
        # Управление
        self.da = 0
        self.dx = 0
        self.dy = 0

    def update(self, keys, isd):
        if isd:
            if keys[pg.K_UP]:
                self.dx += -self.speed * math.sin(math.radians(self.angle))
                self.dy += -self.speed * math.cos(math.radians(self.angle))
            if keys[pg.K_DOWN]:
                self.dx += self.speed * math.sin(math.radians(self.angle))
                self.dy += self.speed * math.cos(math.radians(self.angle))
            if keys[pg.K_LEFT]:
                self.da += self.drag
            if keys[pg.K_RIGHT]:
                self.da -= self.drag
        if not (keys[pg.K_UP] or keys[pg.K_DOWN]):
            self.dx *= 0.95
            self.dy *= 0.95
            self.da *= 0.95
        if abs(self.dx) < 0.2:
            self.dx = 0
        if abs(self.dy) < 0.2:
            self.dy = 0
        self.move()

    def move(self):
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.angle += self.da


if __name__ == "__main__":
    pg.init()
    # Разрешение
    info = pg.display.Info()
    screenw = info.current_w
    screenh = info.current_h
    size = (screenw, screenh)
    screen = pg.display.set_mode(size)
    # Фпс
    v = 30
    clock = Clock()

    all_sprites = pg.sprite.Group()
    screen.fill((0, 0, 0))
    board = Board(screen, "newmap")
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] in keys or keys[pg.K_DOWN] in keys or keys[pg.K_LEFT] in keys or keys[
            pg.K_RIGHT] in keys:
            all_sprites.update(keys, True)
        elif keys[pg.K_UP] in keys or keys[pg.K_DOWN] in keys or keys[pg.K_LEFT] in keys or keys[
            pg.K_RIGHT] in keys:
            all_sprites.update(keys, True)
        screen.fill((0, 0, 0))
        board.render()
        all_sprites.draw(screen)
        pg.display.flip()
        clock.tick(v)
