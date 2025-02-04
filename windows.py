import sys
import pygame as pg
import random
import os
import game

def play_button_sound():
    button_sound.set_volume(0.5)
    button_sound.play()

def loadWin(screenw, screenh):
    pg.mixer.music.load("sounds/vpk-klinok-russkaya-rat-mp3.mp3")
    pg.mixer.music.play(-1)
    logoSurf = pg.image.load('images/logo.png')
    logoSurf = pg.transform.scale(logoSurf, (screenw + 100, screenh))
    logoRect = logoSurf.get_rect(center=(screenw // 2, screenh // 2))
    surf = pg.Surface(size)
    surf.fill("black")
    surfRect = surf.get_rect(center=(screenw // 2, screenh // 2))
    pg.mixer.music.fadeout(6000)

    for i in range(1, 510):
        if i <= 255:
            surf.set_alpha(255 - i)
        else:
            surf.set_alpha((255 - i) * -1)

        screen.blit(logoSurf, logoRect)
        screen.blit(surf, surfRect)
        pg.display.flip()
        pg.time.delay(1)

        for event in pg.event.get():
            if event.type == pg.KEYDOWN or event.type == pg.QUIT:
                pg.mixer.music.stop()
                return
    pg.time.delay(500)

def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image.set_colorkey(colorkey)
    return image


def start_screen(screenw, screenh):
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
                    play_button_sound()
                    for boolet in boolets:
                        boolet.kill()
                    return 3
                if ((screenw - 200 <= x) and (x <= screenw)) and ((0 <= y) and (y <= 200)):
                    play_button_sound()
                    for boolet in boolets:
                        boolet.kill()
                    return 2
                if (exit_text_x - 10 <= x and x <= exit_text_x + exit_text.get_width() + 10) and \
                        (exit_text_y - 10 <= y and y <= exit_text_y + exit_text.get_height() + 10):
                    play_button_sound()
                    return False
        pg.display.update()
        pg.display.flip()


def settings_screen(screenw, screenh):
    volume = 0.1
    fps = 60
    pg.mixer.music.set_volume(volume)

    screen.fill((0, 0, 0))
    for i in range(20):
        Circle(all_sprites)

    font = pg.font.Font(None, 100)
    text = font.render("Настройки", True, (100, 255, 100))
    text_rect = text.get_rect(center=(screenw // 2, screenh // 4 - 100))

    back_button = font.render("Назад", True, (100, 255, 100))
    back_x = screenw // 2 - back_button.get_width() // 2
    back_y = screenh // 2 - back_button.get_height() // 2 + 200

    Vol_button = font.render("Звук", True, (100, 255, 100))
    vol_x = screenw // 2 - 350
    vol_y = screenh // 2 - 80

    slider_x = screenw // 2 - 150
    slider_y = screenh // 2 - 50
    slider_width = 300
    slider_height = 20

    fps_button_text = font.render(f"FPS: {fps}", True, (100, 255, 100))
    fps_button_x = screenw // 2 - 440
    fps_button_y = screenh // 2 + 65

    fps_slider_x = screenw // 2 - 150
    fps_slider_y = screenh // 2 + 100
    fps_slider_width = 300
    fps_slider_height = 20

    while True:
        dt = clock.tick(v)
        screen.blit(text, text_rect)
        screen.blit(back_button, (back_x, back_y))
        screen.blit(Vol_button, (vol_x, vol_y))
        screen.blit(fps_button_text, (fps_button_x, fps_button_y))

        pg.draw.rect(screen, (200, 200, 200), (slider_x, slider_y, slider_width, slider_height))
        pg.draw.rect(screen, (0, 255, 0), (slider_x, slider_y, slider_width * volume, slider_height))

        pg.draw.rect(screen, (200, 200, 200), (fps_slider_x, fps_slider_y, fps_slider_width, fps_slider_height))
        pg.draw.rect(screen, (0, 255, 0), (fps_slider_x, fps_slider_y, fps_slider_width * (fps / 120), fps_slider_height))

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

                if (back_x - 10 <= x <= back_x + back_button.get_width() + 10) and \
                        (back_y - 10 <= y <= back_y + back_button.get_height() + 10):
                    play_button_sound()
                    return 1

                if (slider_x <= x <= slider_x + slider_width) and (slider_y <= y <= slider_y + slider_height):
                    play_button_sound()
                    volume = (x - slider_x) / slider_width
                    pg.mixer.music.set_volume(volume)

                if (fps_slider_x <= x <= fps_slider_x + fps_slider_width) and (fps_slider_y <= y <= fps_slider_y + fps_slider_height):
                    play_button_sound()
                    fps = int(((x - fps_slider_x) / fps_slider_width) * 120)
                    fps_button_text = font.render(f"FPS: {fps}", True, (100, 255, 100))

        pg.display.update()
        pg.display.flip()


class Circle(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.color = (255, 0, 0)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.radius = 5
        self.add(boolets)
        self.x = random.randint(self.radius, screenw - self.radius)
        self.y = random.randint(self.radius, screenh - self.radius)
        self.rect = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self, dt):
        self.rect = self.rect.move(self.dx * dt, self.dy * dt)
        if self.rect.bottom > screenh or self.rect.top < 0:
            self.dy = -self.dy
        if self.rect.left < 0 or self.rect.right > screenw:
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


if __name__ == "__main__":
    pg.init()
    # Группы спрайтов
    button_sound = pg.mixer.Sound("sounds/кнопка2.mp3")
    all_sprites = pg.sprite.Group()
    boolets = pg.sprite.Group()
    # Разрешение
    size = (1000, 1000)
    screenw = size[0]
    screenh = size[1]
    screen = pg.display.set_mode(size)

    loadWin(screenw, screenh)
    # Фпс
    v = 144
    clock = pg.time.Clock()
    # Поверхность для трасеров кружков
    trail_surface = pg.Surface(size)
    trail_surface.fill((0, 0, 0))
    trail_surface.set_alpha(99)
    # Музыка
    pg.mixer.music.load("sounds/фон.mp3")
    pg.mixer.music.set_volume(0.1)
    pg.mixer.music.play(-1, fade_ms=2000)

    state = 1
    while state:
        if state == 1:
            state = start_screen(screenw, screenh)
        if state == 2:
            state = settings_screen(screenw, screenh)
        if state == 3:
            gamec = game.Game(size)
            state = gamec.mainloop()

    pg.quit()
    sys.exit()
