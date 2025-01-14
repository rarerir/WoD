import sys
import pygame as pg
from pygame import Clock
from math import floor
import pickle
import random


def calculate_move_vect(speed, angle_in_degrees):
    move_vec = pg.math.Vector2()
    move_vec.from_polar((speed, angle_in_degrees))
    return move_vec

class Board:
    # Создание поля
    def __init__(self, canvas, mapn, cell_size=30):
        self.load(mapn)
        self.canvas = canvas
        self.colors = ["black", "brown", "blue"]
        self.cell_size = cell_size
        # Отцентровывание
        self.left = (screenw - self.x * cell_size) / 2
        self.top = (screenh - self.y * cell_size) / 2
        if self.left < 0:
            self.cell_size = floor(screenw / self.x)
            self.left = (screenw - self.x * self.cell_size) / 2
        if self.top < 0:
            if self.cell_size > floor(screenh / self.y):
                self.cell_size = floor(screenh / self.y)
            # Отступы
            self.top = (screenh - self.y * self.cell_size) / 2
        self.left = (screenw - self.x * self.cell_size) / 2
        # Спавн игроков
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
        self.tank1 = Tank((450, 450), 1, 3, 3)


class Border(pg.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pg.Surface([1, y2 - y1])
            self.rect = pg.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pg.Surface([x2 - x1, 1])
            self.rect = pg.Rect(x1, y1, x2 - x1, 1)

    def draw(self):
        pg.draw.line(screen, "white", (self.x1, self.y1), (self.x2, self.y2), 30)


class Tank(pg.sprite.Sprite):
    def __init__(self, spawn, speed, angspeed, hp):
        super().__init__(all_sprites, tanks)
        # Програмные
        self.original_image = pg.image.load('sprites/крутой так.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center=spawn)
        self.pos = spawn
        # Игровые
        self.hp = hp
        self.angle = 0
        self.angspeed = angspeed * 0.1
        self.speed = speed
        # Управление
        self.dx = 0
        self.dy = 0

    def update(self, keys, isd):
        if isd:
            fps = self.speed * dt
            angfps = int(self.angspeed * dt)
            if keys[pg.K_UP]:
                xy = calculate_move_vect(-fps, -self.angle + 90)
                self.dx += xy[0]
                self.dy += xy[1]
            elif keys[pg.K_DOWN]:
                # не обращайте внимания на повторы это оптимизация так надо
                xy = calculate_move_vect(fps, -self.angle + 90)
                self.dx += xy[0]
                self.dy += xy[1]
            if keys[pg.K_LEFT]:
                self.angle += angfps
            elif keys[pg.K_RIGHT]:
                self.angle -= angfps
            if keys[pg.K_SPACE]:
                self.shoot(fps)
        self.collisions()
        self.move()

    def collisions(self):
        collisions = pg.sprite.spritecollide(self, all_sprites, False)
        if len(collisions) > 1:
            colidehor, colidever = pg.sprite.spritecollideany(self, horizontal_borders), pg.sprite.spritecollideany(self, vertical_borders)
            if colidehor or colidever:
                if colidehor:
                    if self.dy < 0:
                        self.dy = -self.dy + 5
                    elif self.dy >= 0:
                        self.dy = -self.dy - 5
                elif colidever:
                    if self.dx < 0:
                        self.dx = -self.dx + 5
                    elif self.dx >= 0:
                        self.dx = -self.dx - 5
                self.angle += 180
            bulcol = pg.sprite.spritecollide(self, boolets, False)
            for boolet in range(len(bulcol)):
                self.hp -= 1
                print(self.hp)
                bulcol[boolet].explode()

            if self.hp <= 0:
                self.explode()

    def shoot(self, speed):
        Boolet(speed * 2, self.angle, self.rect.center)


    def move(self):
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.pos = (self.rect.x, self.rect.y)
        self.dx = 0
        self.dy = 0
        self.angle = self.angle % 360

    def explode(self):
        Explosion(self, self.rect.center, 100)


class Boolet(pg.sprite.Sprite):
    def __init__(self, speed, angle, center):
        super().__init__(all_sprites, boolets)
        self.dx, self.dy = calculate_move_vect(speed, angle)
        self.x, self.y = center[0] + self.dy, center[1] + self.dx
        self.radius = 2
        self.add(boolets)
        self.image = pg.image.load('sprites/bullet.png')
        self.image = pg.transform.scale(self.image, (self.radius, self.radius))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect = self.rect.move(self.dx, self.dy)
        if pg.sprite.spritecollideany(self, horizontal_borders):
            self.dy = -self.dy
        if pg.sprite.spritecollideany(self, vertical_borders):
            self.dx = -self.dx
        colided = pg.sprite.spritecollideany(self, boolets)
        if colided != self:
            colided.explode()
            self.explode()
        self.collisions()

    def collisions(self):
        collisions = pg.sprite.spritecollide(self, all_sprites, False)
        if len(collisions) > 1:
            colidehor, colidever = pg.sprite.spritecollideany(self, horizontal_borders), pg.sprite.spritecollideany(self, vertical_borders)
            if colidehor or colidever:
                if colidehor:
                    if self.dy < 0:
                        self.dy = -self.dy + 5
                    elif self.dy >= 0:
                        self.dy = -self.dy - 5
                elif colidever:
                    if self.dx < 0:
                        self.dx = -self.dx + 5
                    elif self.dx >= 0:
                        self.dx = -self.dx - 5

    def draw(self, surface):
        pg.draw.circle(surface, self.color, self.rect.center, self.radius)

    def explode(self):
        Explosion(self, self.rect.center, 36)


class Explosion(pg.sprite.Sprite):
    def __init__(self, thing, center, power, duration=100):
        super().__init__(all_sprites, explosions)
        self.image = pg.image.load('sprites/explosion.jpg')
        self.rect = self.image.get_rect(center=center)
        self.thing = thing
        self.power = power // duration
        self.dispersion = 0
        self.duration = duration
        self.thing.kill()

    def update(self, surface):
        self.dispersion += self.power
        self.duration -= 1
        if self.duration == 0:
            self.kill()
        self.image = pg.transform.scale(self.image, (self.dispersion * 3, self.dispersion * 3))
        self.rect = self.image.get_rect(center=self.rect.center)
        print(self.rect.center)


if __name__ == "__main__":
    pg.init()
    # Разрешение
    info = pg.display.Info()
    screenw = info.current_w
    screenh = info.current_h
    size = (screenw, screenh)
    screen = pg.display.set_mode(size)
    # Группы спрайтов
    all_sprites = pg.sprite.Group()
    vertical_borders, horizontal_borders = pg.sprite.Group(), pg.sprite.Group()
    tanks = pg.sprite.Group()
    boolets = pg.sprite.Group()
    explosions = pg.sprite.Group()
    # Границы
    Border(5, 5, screenw - 5, 5)
    Border(5, screenh - 5, screenw - 5, screenh - 5)
    Border(5, 5, 5, screenh - 5)
    Border(screenw - 5, 5, screenw - 5, screenh - 5)

    screen.fill((0, 0, 0))

    running = True
    # Фпс
    v = 60
    clock = Clock()

    board = Board(screen, "newmap")
    while running:
        dt = clock.tick(v)
        screen.fill((0, 0, 0))
        board.render()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        for border in horizontal_borders:
            border.draw()
        for border in vertical_borders:
            border.draw()
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_DOWN] or keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
            tanks.update(keys, True)
        boolets.update()
        explosions.update(screen)
        all_sprites.draw(screen)
        pg.display.flip()
