import sys
import pygame as pg
from pygame.time import Clock
import os

def loadWin(size, screenw, screenh):
    logoSurf = pg.image.load('images/logo.png')
    logoRect = logoSurf.get_rect(center=(screenw // 2, screenh // 2))
    surf = pg.Surface(size)
    surf.fill("black")
    surfRect = surf.get_rect(center=(screenw // 2, screenh // 2))
    for i in range(1, 510):
        if i <= 255:
            surf.set_alpha(255 - i)
        else:
            surf.set_alpha((255 - i) * -1)
        screen.blit(logoSurf, logoRect)
        screen.blit(surf, surfRect)
        pg.display.flip()
        pg.time.delay(1)

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
    fon = pg.transform.scale(load_image('фон_1.gif'), (screenw, screenh))
    settings = pg.transform.scale(load_image('настройки.png'), (200, 200))
    screen.blit(fon, (0, 0))
    screen.blit(settings, (screenw - 200, 0))

    font = pg.font.Font(None, 200)
    text = font.render("ИГРАТЬ", True, (100, 255, 100))
    text_x = screenw // 2 - text.get_width() // 2
    text_y = screenh // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pg.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

    exit_font = pg.font.Font(None, 100)
    exit_text = exit_font.render("ВЫЙТИ", True, (100, 255, 100))
    exit_text_x = screenw // 2 - exit_text.get_width() // 2
    exit_text_y = text_y + text.get_height() + 50
    screen.blit(exit_text, (exit_text_x, exit_text_y))
    pg.draw.rect(screen, (0, 255, 0), (exit_text_x - 10, exit_text_y - 10,
                                       exit_text.get_width() + 20, exit_text.get_height() + 20), 1)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                if ((text_x - 10 <= x) and (x <= text_x + text_w + 10)) and ((
                        text_y - 10 <= y) and (y <= text_y + text_h + 10)):
                    return
                if ((screenw - 200 <= x) and (x <= screenw)) and ((0 <= y) and (y <= 200)):
                    settings_screen(size, screenw, screenh)
                if (exit_text_x - 10 <= x  and x <= exit_text_x + exit_text.get_width() + 10) and \
                        (exit_text_y - 10 <= y and y <= exit_text_y + exit_text.get_height() + 10):
                    pg.quit()
                    sys.exit()
        pg.display.flip()
        clock.tick(v)

def settings_screen(size, screenw, screenh):
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
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                if (back_x - 10 <= x and x <= back_x + back_button.get_width() + 10) and (
                        back_y - 10 <= y and y <= back_y + back_button.get_height() + 10):
                    start_screen(size, screenw, screenh)

        pg.display.flip()
        clock.tick(v)


def calculate_move_vect(speed, angle_in_degrees):
    move_vec = pg.math.Vector2()
    move_vec.from_polar((speed, angle_in_degrees))
    return move_vec

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
    explosions = pg.sprite.Group()

    screen.fill((0, 0, 0))

    # FPS
    running = True
    v = 144
    clock = Clock()

    # Загрузка заставки
    loadWin(size, screenw, screenh)

    # Запуск заставочного экрана
    start_screen(size, screenw, screenh)

    while running:
        dt = clock.tick(v)
        screen.fill((0, 0, 0))
        # Эвенты
        events = pg.event.get()
        keys = pg.key.get_pressed()
        for event in events:
            if event.type == pg.QUIT:
                running = False

        # Обновление спрайтов
        all_sprites.update((keys, events))
        all_sprites.draw(screen)

        pg.display.flip()

    pg.quit()
