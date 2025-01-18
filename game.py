import sys
import pygame as pg
from pygame.time import Clock
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
        self.tank1 = Tank((450, 450), 0.5, 3, 3, image="танчик2.png")
        self.tank2 = Tank((550, 550), 0.5, 3, 3, key_forward=pg.K_w,
                 key_backward=pg.K_s, key_left=pg.K_a, key_right=pg.K_d, key_shoot=pg.K_e, image='танчик1.png')


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
    def __init__(self, spawn, speed, angspeed, hp, size=(60, 80), ammorecharge=1, maxammo=5, key_forward=pg.K_UP,
                 key_backward=pg.K_DOWN, key_left=pg.K_LEFT, key_right=pg.K_RIGHT, key_shoot=pg.K_SPACE,
                 image='крутой так.png'):
        super().__init__(all_sprites, tanks)
        # Игровые
        self.ammorecharge = ammorecharge
        self.maxammo = maxammo
        self.currentammo = maxammo
        self.hp = hp
        self.angle = 0
        self.angspeed = angspeed * 0.1
        self.speed = speed
        self.size = size
        self.original_image = pg.image.load(f'sprites/{image}')
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

    def update(self, keys):
        fps = self.speed * dt
        angfps = int(self.angspeed * dt)
        if keys[0][self.key_forward]:
            xy = calculate_move_vect(-fps, -self.angle + 90)
            self.dx += xy[0]
            self.dy += xy[1]
        elif keys[0][self.key_backward]:
            xy = calculate_move_vect(fps, -self.angle + 90)
            self.dx += xy[0]
            self.dy += xy[1]
        if keys[0][self.key_left]:
            self.angle += angfps
        elif keys[0][self.key_right]:
            self.angle -= angfps

        for event in keys[1]:
            if event.type == pg.KEYDOWN and event.dict.get("key") == self.key_shoot and self.currentammo > 0:
                self.shoot()
        if self.currentammo < self.maxammo:
            self.currentammo += dt * self.ammorecharge
        self.move()
        self.collisions()

    def collisions(self):
        colidehor = pg.sprite.spritecollideany(self, horizontal_borders)
        colidever = pg.sprite.spritecollideany(self, vertical_borders)

        if colidehor:
            if self.dy < 0:
                self.rect.top = colidehor.rect.bottom
            elif self.dy > 0:
                self.rect.bottom = colidehor.rect.top
            self.dy = 0

        if colidever:
            if self.dx < 0:
                self.rect.left = colidever.rect.right
            elif self.dx > 0:
                self.rect.right = colidever.rect.left
            self.dx = 0
        for boolet in boolets:
            if pg.sprite.collide_mask(self, boolet):
                self.hp -= 1
                print(self.hp)
                boolet.explode()

        if self.hp <= 0:
            self.explode()

        self.check_boundaries()

    def check_boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenw:
            self.rect.right = screenw
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screenh:
            self.rect.bottom = screenh

    def shoot(self):
        self.currentammo -= 1
        spawn_position = (
            self.rect.centerx + calculate_move_vect(-self.size[1], -self.angle + 90)[0],
            self.rect.centery + calculate_move_vect(-self.size[1], -self.angle + 90)[1]
        )
        Boolet(self.speed * 1.5, self.angle, spawn_position)

    def move(self):
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.dx = 0
        self.dy = 0
        self.angle = self.angle % 360

    def explode(self):
        Explosion(self, self.rect.center, 100)


class Boolet(pg.sprite.Sprite):
    def __init__(self, speed, angle, center):
        super().__init__(all_sprites, boolets)
        # Игровые
        self.radius = 20
        self.speed = speed
        self.angle = angle
        self.hp = 3

        # Спавн
        self.add(boolets)
        self.x, self.y = calculate_move_vect(-(self.speed * dt), -self.angle + 90) + center

        # Картинка
        self.original_image = pg.image.load('sprites/bullet.png')
        self.original_image = pg.transform.scale(self.original_image, (self.radius, self.radius))
        self.image = self.original_image
        self.image = pg.transform.rotate(self.original_image, angle + 90)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, events):
        fps = self.speed * dt
        self.xy = calculate_move_vect(-fps, -self.angle + 90)
        self.move()
        self.collisions()

    def move(self):
        self.image = pg.transform.rotate(self.original_image, self.angle + 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center += self.xy
        self.pos = (self.rect.x, self.rect.y)
        self.angle = self.angle

    def collisions(self):
        if pg.sprite.spritecollideany(self, horizontal_borders):
            self.angle += 90
        if pg.sprite.spritecollideany(self, vertical_borders):
            self.angle += 90

        bulcol = pg.sprite.spritecollide(self, boolets, False)
        if len(bulcol) > 1:
            for boolet in bulcol:
                boolet.explode()

        if self.hp <= 0:
            self.explode()


    def explode(self):
        Explosion(self, self.rect.center, 100)


class Explosion(pg.sprite.Sprite):
    image = pg.image.load('sprites/explosion.jpg')
    image = pg.transform.scale(image, (10, 10))

    def __init__(self, thing, center, power, duration=100):
        super().__init__(all_sprites, explosions)
        self.power = power // duration
        self.rect = self.image.get_rect(center=center)
        self.thing = thing
        self.dispersion = 0
        self.duration = duration
        self.thing.kill()

    def update(self, events):
        self.dispersion += self.power
        self.duration -= 1
        if self.duration == 0:
            self.kill()
        self.image = pg.transform.scale(self.image, (self.dispersion * 3, self.dispersion * 3))
        self.rect = self.image.get_rect(center=self.rect.center)


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

    # Фпс
    running = True
    v = 144
    clock = Clock()

    board = Board(screen, "newmap")
    while running:
        dt = clock.tick(v)
        screen.fill((0, 0, 0))
        board.render()
        # Эвенты
        events = pg.event.get()
        keys = pg.key.get_pressed()
        for event in events:
            if event.type == pg.QUIT:
                running = False

        for border in horizontal_borders:
            border.draw()
        for border in vertical_borders:
            border.draw()
        # Обновление спрайтов
        all_sprites.update((keys, events))
        all_sprites.draw(screen)

        pg.display.flip()
