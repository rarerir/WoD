import sys
import pygame as pg
from pygame import Clock
from math import floor
import pickle
import random
import math


class Board:
    # Создание поля
    def __init__(self, canvas, mapn, cell_size=30):
        self.load(mapn)
        self.canvas = canvas
        self.colors = ["black", "brown", "blue"]
        self.cell_size = cell_size
        self.left = (screenw - self.x * cell_size) / 2
        self.top = (screenh - self.y * cell_size) / 2
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
        print(mapstr)

    def spawn(self):
        spawn = (random.randrange(1, self.x + 1), random.randrange(1, self.y + 1))
        self.tank1 = Tank(spawn, 3, all_sprites)


class Tank(pg.sprite.Sprite):
    def __init__(self, spawn, colorid, *group):
        super().__init__(*group)
        self.original_image = pg.image.load('sprites/крутой так.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect = pg.Rect(self.rect.y, self.rect.x, self.rect.h, self.rect.w)
        self.colorid = colorid
        self.spawn = spawn
        self.angle = 0
        self.speed = 4
        print(self.spawn)

    def update(self, keys, isd):


    def move(self):
        if keys[pg.K_UP]:
            self.move(self.speed)
        if keys[pg.K_DOWN]:
            self.move(-self.speed)
        if keys[pg.K_LEFT]:
            self.angle += 5
        if keys[pg.K_RIGHT]:
            self.angle -= 5
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)



if __name__ == "__main__":
    pg.init()
    # Разрешение
    info = pg.display.Info()
    screenw = info.current_w
    screenh = info.current_h
    size = (screenw, screenh)
    screen = pg.display.set_mode(size)
    # Фпс
    v = 90
    clock = Clock()

    all_sprites = pg.sprite.Group()
    screen.fill((0, 0, 0))
    board = Board(screen, "newmap")
    running = True
    while running:
        for event in pg.event.get():
            keys = pg.key.get_pressed()
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                board.tank1.update(keys, True)
            elif event.type == pg.KEYUP:
                board.tank1.update(keys, False)
        screen.fill((0, 0, 0))
        board.render()
        all_sprites.draw(screen)
        board.tank1.update
        pg.display.flip()
        clock.tick(v)