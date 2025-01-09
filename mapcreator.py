import pygame as pg
from math import floor
import pickle


class Board:
    # создание поля
    def __init__(self, width, height, canvas, cell_size=30):
        self.width = width
        self.height = height
        self.canvas = canvas
        self.colors = ["black", "brown", "blue"]
        self.board = [[0] * width for _ in range(height)]
        self.cell_size = cell_size
        self.left = (screenw - x * cell_size) / 2
        self.top = (screenh - y * cell_size) / 2
        if self.left < 0:
            self.cell_size = floor(screenw / x)
            self.left = (screenw - x * self.cell_size) / 2
        if self.top < 0:
            if self.cell_size > floor(screenh / y):
                self.cell_size = floor(screenh / y)
            self.top = (screenh - y * self.cell_size) / 2
        self.left = (screenw - x * self.cell_size) / 2

    def render(self):
        for i in range(int(self.height)):
            for j in range(int(self.width)):
                eq = (j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size, self.cell_size)
                pg.draw.rect(self.canvas, self.colors[self.board[i][j]], eq)
                pg.draw.rect(self.canvas, 'white', eq, 1)

    def get_cell(self, coords):
        x, y = coords
        pos_x = (x - self.left) // self.cell_size
        pos_y = (y - self.top) // self.cell_size
        if pos_y in range(self.height) and pos_x in range(self.width):
            return (int(pos_x), int(pos_y))
        else:
            return None

    def on_click(self, cell_coords):
        x, y = cell_coords[0], cell_coords[1]
        self.board[y][x] = (self.board[y][x] + 1) % 3

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def save(self):
        with open(f'maps/{input("Введите название карты").replace(" ", "").replace(":", "")}.wmap', "wb") as f:
            self.board.append([x, y])
            pickle.dump(self.board, f)
            print("Карта сохранена")


if __name__ == "__main__":
    pg.init()
    cells = tuple(map(int, input("Введите кол-во клеток по x и y соответственно (через пробел): \n").split()))
    x = cells[0]
    y = cells[1]
    info = pg.display.Info()
    screenw = info.current_w
    screenh = info.current_h
    running = True
    size = (screenw, screenh)
    screen = pg.display.set_mode(size)
    screen.fill((0, 0, 0))
    board = Board(x, y, screen)
    board.render()
    print("Для того что-бы сохранить нажмите enter")
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.dict.get("key") == 13:
                board.save()
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
                screen.fill((0, 0, 0))
                board.render()
        pg.display.flip()