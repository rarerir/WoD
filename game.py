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


# экран загрузочный ну или просто отображение компании
def loadWin(size, screenw, screenh):
    stop = False
    logoSurf = pg.image.load('images/logo.png')
    logoRect = logoSurf.get_rect(center = (screenw//2, screenh//2))
    surf = pg.Surface(size)
    surf.fill("black")
    surfRect = surf.get_rect(center = (screenw//2, screenh//2))
    for i in range(1, 510):
        if stop:
            break
        if i <= 255:
            surf.set_alpha(255 - i)
        else:
            surf.set_alpha((255 - i)*-1)
        screen.blit(logoSurf, logoRect)
        screen.blit(surf, surfRect)
        pg.display.flip()
        for j in pg.event.get():
            if j.type == pg.KEYDOWN:
                stop = True
                break


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
        self.load(mapn)
        self.types = [0, 1, 2]
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
        for i in range(int(self.y)):
            for j in range(int(self.x)):
                eq = (j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size)
                self.board[i][j] = Cell(eq, self.board, (i, j), self.types[self.board[i][j]], cell_size=self.cell_size)
        # Спавн игроков
        self.spawn()

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


class Cell(pg.sprite.Sprite):
    images = ['sprites/земля.jpg', 'sprites/кирпичи.png', 'sprites/вода.jpg', 'sprites/коробка.jpg']

    def __init__(self, eq, board, pos, type=1, cell_size=30):
        super().__init__(all_sprites, cells)
        self.type = type
        self.image = pg.image.load(f'{self.images[self.type]}')
        self.image = pg.transform.scale(self.image, (cell_size, cell_size))
        self.rect = self.image.get_rect(x=eq[0], y=eq[1])
        self.mask = pg.mask.from_surface(self.image)
        # Надо доделать
        self.board = board
        self.pos = pos

        if self.type != 0:
            if self.type != 2:
                cells_colideable_b.add(self)
            cells_colideable_t.add(self)

    def get_sides(self):
        return (Vector2(self.rect.topleft), Vector2(self.rect.bottomleft), Vector2(self.rect.topright),
                Vector2(self.rect.bottomright))


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
    def __init__(self, spawn, speed, angspeed, hp, size=(50, 50), ammorecharge=1, maxammo=5, key_forward=pg.K_UP,
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

    def update(self, keys, dt):
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

        for event in keys[1]:
            if event.type == pg.KEYDOWN and event.dict.get("key") == self.key_shoot and self.currentammo > 0:
                self.shoot(dt)
        if self.currentammo < self.maxammo:
            self.currentammo += dt * self.ammorecharge
        self.collisions()
        self.move()

    def collisions(self):
        self.check_boolets()
        self.check_cells()
        self.check_boundaries()

    def check_boolets(self):
        for boolet in boolets:
            if pg.sprite.collide_mask(self, boolet):
                self.hp -= 1
                print(self.hp)
                boolet.explode()

        if self.hp <= 0:
            self.explode()

    def check_cells(self):
        collided_cell = pg.sprite.spritecollideany(self, cells_colideable_t)
        if collided_cell:
            topleft, bottomleft, topright, bottomright = collided_cell.get_sides()
            linestart = Vector2(floor(self.rect.center[0] - self.dx), floor(self.rect.center[1] - self.dy))
            lineend = Vector2(self.rect.center[0], self.rect.center[1])
            # Верх
            if intersection(topleft, topright, linestart, lineend):
                print("up")
                self.rect.bottom = collided_cell.rect.top
            # Низ
            if intersection(bottomleft, bottomright, linestart, lineend):
                print("bottom")
                self.rect.top = collided_cell.rect.bottom
            # Лево
            if intersection(topleft, bottomleft, linestart, lineend):
                print("left")
                self.rect.right = collided_cell.rect.left
            # Право
            if intersection(topright, bottomright, linestart, lineend):
                print("right")
                self.rect.left = collided_cell.rect.right

        # collided_cell = pg.sprite.spritecollideany(self, cells_colideable_t)
        #
        # if collided_cell:
        #     if self.dx > 0:
        #         self.rect.right = collided_cell.rect.left
        #     elif self.dx < 0:
        #         self.rect.left = collided_cell.rect.right
        #
        #     if self.dy > 0:
        #         self.rect.bottom = collided_cell.rect.top
        #     elif self.dy < 0:
        #         self.rect.top = collided_cell.rect.bottom

    def check_boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenw:
            self.rect.right = screenw
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screenh:
            self.rect.bottom = screenh

    def shoot(self, dt):
        shoot_channel = pg.mixer.Channel(1)
        shoot_sound = pg.mixer.Sound("sounds/выстрел.mp3")
        shoot_channel.play(shoot_sound)
        self.currentammo -= 1
        spawn_position = (
            self.rect.centerx + calculate_move_vect(-self.size[1], -self.angle + 90)[0],
            self.rect.centery + calculate_move_vect(-self.size[1], -self.angle + 90)[1]
        )
        Boolet(self.speed * 1.3, self.angle, spawn_position, dt)

    def move(self):
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.dx = 0
        self.dy = 0
        self.angle = self.angle % 360

    def explode(self):
        Explosion(self, self.rect.center, 100)


class Boolet(pg.sprite.Sprite):
    def __init__(self, speed, angle, center, dt):
        super().__init__(all_sprites, boolets)
        # Игровые
        self.radius = 20
        self.speed = speed
        self.angle = angle
        self.hp = 3

        # Спавн
        self.add(boolets)
        vector = calculate_move_vect(-self.speed * dt, angle)
        self.clockvector = Vector2(0, 1)
        x, y = vector + center
        self.dy, self.dx = vector

        # Картинка
        self.original_image = pg.image.load('sprites/bullet.png')
        self.original_image = pg.transform.scale(self.original_image, (self.radius, self.radius))
        self.image = self.original_image
        self.image = pg.transform.rotate(self.original_image, self.angle + 90)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, events, dt):
        self.collisions()
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.angle = self.angle_hand()
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)  # Rotate the image
        self.rect = self.image.get_rect(center=self.rect.center)

    def angle_hand(self):
        # Calculate the angle based on the dx and dy movement
        angle = math.degrees(math.atan2(self.dx, self.dy))
        return angle % 360

    def collisions(self):
        self.check_boolets()
        self.check_cells()
        self.check_boundaries()

    def check_boolets(self):
        bulcol = pg.sprite.spritecollide(self, boolets, False)
        if len(bulcol) > 1:
            for boolet in bulcol:
                boolet.explode()

    def check_cells(self):
        collided_cell = pg.sprite.spritecollideany(self, cells_colideable_b)
        if collided_cell:
            topleft, bottomleft, topright, bottomright = collided_cell.get_sides()
            linestart = Vector2(floor(self.rect.center[0] - self.dx), floor(self.rect.center[1] - self.dy))
            lineend = Vector2(self.rect.center[0], self.rect.center[1])
            # Верх
            if intersection(topleft, topright, linestart, lineend):
                print("up")
                self.dy = -self.dy
                self.rect.top = collided_cell.rect.top - self.rect.height
            # Низ
            elif intersection(bottomleft, bottomright, linestart, lineend):
                print("bottom")
                self.dy = -self.dy
                self.rect.bottom = collided_cell.rect.bottom + self.rect.height
            # Лево
            if intersection(topleft, bottomleft, linestart, lineend):
                print("left")
                self.dx = -self.dx
                self.rect.left = collided_cell.rect.left - self.rect.width
            # Право
            elif intersection(topright, bottomright, linestart, lineend):
                print("right")
                self.dx = -self.dx
                self.rect.right = collided_cell.rect.right + self.rect.width

    def check_boundaries(self):
        if pg.sprite.spritecollideany(self, horizontal_borders):
            self.dy = -self.dy
            self.angle = -self.angle + 180
        if pg.sprite.spritecollideany(self, vertical_borders):
            self.dx = -self.dx
            self.angle = -self.angle % 360
            self.hp -= 1
        if self.hp == 0:
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

    def update(self, events, dt):
        self.dispersion += self.power
        self.duration -= 1
        if self.duration == 0:
            self.kill()
        self.image = pg.transform.scale(self.image, (self.dispersion, self.dispersion))
        self.rect = self.image.get_rect(center=self.rect.center)


class Game:
    def __init__(self):
        global screenw, screenh, screen, all_sprites, vertical_borders, horizontal_borders, cells, cells_colideable_t
        global cells_colideable_b, tanks, boolets, explosions, clock, v

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
        cells, cells_colideable_t, cells_colideable_b = pg.sprite.Group(), pg.sprite.Group(), pg.sprite.Group()
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
        v = 144
        clock = Clock()

    def mainloop(self):
        running = True
        board = Board("newmap")
        while running:
            dt = clock.tick(v)
            screen.fill((0, 0, 0))
            # Эвенты
            events = pg.event.get()
            keys = pg.key.get_pressed()
            for event in events:
                if event.type == pg.QUIT:
                    return False

            for border in horizontal_borders:
                border.draw()
            for border in vertical_borders:
                border.draw()
            # Обновление спрайтов
            all_sprites.update((keys, events), dt)
            all_sprites.draw(screen)

            pg.display.flip()


if __name__ == "__main__":
    game = Game()
    game.mainloop()