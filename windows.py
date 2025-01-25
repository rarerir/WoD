import sys
import pygame as pg
import random
import os
import game


def loadWin(size, screenw, screenh):
    #1530 830\
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


def start_screen(size, screenw, screenh):
    screen.fill((0, 0, 0))
    settings = pg.transform.scale(load_image('настройки.png'), (200, 200))

    font = pg.font.Font(None, 200)
    text = font.render("ИГРАТЬ", True, (100, 255, 100))
    text_x = screenw // 2 - text.get_width() // 2
    text_y = screenh // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()

    exit_font = pg.font.Font(None, 100)
    exit_text = exit_font.render("ВЫЙТИ", True, (100, 255, 100))
    exit_text_x = screenw // 2 - exit_text.get_width() // 2
    exit_text_y = text_y + text.get_height() + 50
    for i in range(20):
        Circle(all_sprites)

    while True:
        dt = clock.tick(v)
        screen.blit(settings, (screenw - 200, 0))

        screen.blit(text, (text_x, text_y))
        pg.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)
        screen.blit(exit_text, (exit_text_x, exit_text_y))
        pg.draw.rect(screen, (0, 255, 0), (exit_text_x - 10, exit_text_y - 10,
                                           exit_text.get_width() + 20, exit_text.get_height() + 20), 1)

        all_sprites.update(dt)

        trail_surface.fill((0, 0, 0, 0))
        for sprite in boolets:
            sprite.draw(trail_surface)

        screen.blit(trail_surface, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                if ((text_x - 10 <= x) and (x <= text_x + text_w + 10)) and ((text_y - 10 <= y) and (
                        y <= text_y + text_h + 10)):
                    for boolet in boolets:
                        boolet.kill()
                    return 3
                if ((screenw - 200 <= x) and (x <= screenw)) and ((0 <= y) and (y <= 200)):
                    for boolet in boolets:
                        boolet.kill()
                    return 2
                if (exit_text_x - 10 <= x and x <= exit_text_x + exit_text.get_width() + 10) and \
                        (exit_text_y - 10 <= y and y <= exit_text_y + exit_text.get_height() + 10):
                    return False
        pg.display.update()
        pg.display.flip()


def settings_screen(size, screenw, screenh):
    screen.fill((0, 0, 0))
    fon = pg.transform.scale(load_image('фон_1.gif'), (screenw, screenh))
    screen.blit(fon, (0, 0))

    font = pg.font.Font(None, 100)
    text = font.render("Настройки", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screenw // 2, screenh // 4))
    screen.blit(text, text_rect)

    back_button = font.render("Назад", True, (255, 255, 255))
    back_x = screenw // 2 - back_button.get_width() // 2
    back_y = screenh // 2 - back_button.get_height() // 2 + 100
    screen.blit(back_button, (back_x, back_y))
    pg.draw.rect(screen, (0, 255, 0), (back_x - 10, back_y - 10,
                                       back_button.get_width() + 20, back_button.get_height() + 20), 1)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                if (back_x - 10 <= x and x <= back_x + back_button.get_width() + 10) and (
                        back_y - 10 <= y and y <= back_y + back_button.get_height() + 10):
                    return 1

        pg.display.flip()
        clock.tick(v)


class Circle(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.color = (255, 0, 0)
        self.dx = random.choice([-1, 1]) * dt
        self.dy = random.choice([-1, 1]) * dt
        self.radius = 5
        self.add(boolets)
        self.x = random.randint(self.radius, screenw - self.radius)
        self.y = random.randint(self.radius, screenh - self.radius)
        self.rect = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self, dt):
        self.rect = self.rect.move(self.dx * dt, self.dy * dt)
        if pg.sprite.spritecollideany(self, horizontal_borders):
            self.dy = -self.dy
        if pg.sprite.spritecollideany(self, vertical_borders):
            self.dx = -self.dx
        colided = pg.sprite.spritecollideany(self, boolets)
        if colided != self:
            colided.explode()
            self.explode()

    def draw(self, surface):
        pg.draw.circle(surface, self.color, self.rect.center, self.radius)

    def explode(self):
        self.kill()
        Circle(all_sprites)


class Border(pg.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pg.Surface([1, y2 - y1])
            self.rect = pg.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pg.Surface([x2 - x1, 1])
            self.rect = pg.Rect(x1, y1, x2 - x1, 1)


if __name__ == "__main__":
    pg.init()
    # Группы спрайтов
    all_sprites = pg.sprite.Group()
    horizontal_borders = pg.sprite.Group()
    vertical_borders = pg.sprite.Group()
    boolets = pg.sprite.Group()
    # Разрешение
    info = pg.display.Info()
    screenw = info.current_w
    screenh = info.current_h
    size = (screenw, screenh)
    screen = pg.display.set_mode(size)
    # Границы
    Border(5, 5, screenw - 5, 5)
    Border(5, screenh - 5, screenw - 5, screenh - 5)
    Border(5, 5, 5, screenh - 5)
    Border(screenw - 5, 5, screenw - 5, screenh - 5)
    # Фпс
    v = 144
    clock = pg.time.Clock()

    trail_surface = pg.Surface((screenw, screenh))
    trail_surface.fill((0, 0, 0))
    trail_surface.set_alpha(99)
    dt = clock.tick(v) / 10
    gamec = game.Game()

    loadWin(size, screenw, screenh)
    state = 1
    while state:
        if state == 1:
            state = start_screen(size, screenw, screenh)
        if state == 2:
            state = settings_screen(size, screenw, screenh)
        if state == 3:
            state = gamec.mainloop()
    pg.quit()
    sys.exit()