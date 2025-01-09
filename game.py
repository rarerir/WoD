import pygame as pg
from math import floor
import pickle


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

    def render(self):
        for i in range(int(self.y)):
            for j in range(int(self.x)):
                eq = (j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size, self.cell_size)
                pg.draw.rect(self.canvas, self.colors[self.board[i][j]], eq)

    def load(self, mapnm):
        with(open(f'maps/{mapnm}.wmap', "rb")) as f:
            mapstr = pickle.load(f)
        self.x, self.y = mapstr.pop(-1)
        self.board = mapstr
        print(mapstr)


class Tank():
    pass


if __name__ == "__main__":
    pg.init()
    info = pg.display.Info()
    screenw = info.current_w
    screenh = info.current_h
    running = True
    size = (screenw, screenh)
    screen = pg.display.set_mode(size)
    screen.fill((0, 0, 0))
    board = Board(screen, input("Введите название карты\n"))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        board.render()
        pg.display.flip()