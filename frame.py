import pygame as pg
import pygame_gui, sys
from pygame.locals import *

pg.init()
displayIndex = 0
DISPLAYS = [(1024, 576), (1152, 648), (1280, 720), (1600, 900), (1920, 1080), (2560, 1440)]
screen = pg.display.set_mode(DISPLAYS[displayIndex])
screen.fill((0, 0, 0))
imagePath = "sprites/icons8-cursor-24.png"


class Icon(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.smileyImage = pg.image.load(imagePath)
        self.image = self.smileyImage.convert_alpha()
        self.rect = self.image.get_rect()
        self.posX = x
        self.posY = y
        self.rect.x = x
        self.rect.y = y
        self.defaultx = (float(self.rect[2])/DISPLAYS[0][0])*100
        self.defaulty = (float(self.rect[3])/DISPLAYS[0][1])*100

    def updateSize(self):
        self.image = ImageRescaler(self.smileyImage, (self.defaultx, self.defaulty))
        self.rect = self.image.get_rect()
        self.rect.x = self.posX
        self.rect.y = self.posY


class Arrow(pg.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.smileyImage = pg.image.load(imagePath)
        self.defaultx = (float(self.rect[2]) / DISPLAYS[0][0]) * 100
        self.defaulty = (float(self.rect[3]) / DISPLAYS[0][1]) * 100
        self.image = pg.image.load('sprites/icons8-cursor-24.png')
        self.rect = self.image.get_rect()

    def update(self, mouse_pos):
        self.rect.x = mouse_pos[0]
        self.rect.y = mouse_pos[1]

    def updateSize(self):
        self.image = ImageRescaler(self.smileyImage, (self.defaultx, self.defaulty))
        self.rect = self.image.get_rect()
        self.rect.x = mouse_pos[0]
        self.rect.y = mouse_pos[1]


def ImageRescaler(image,originalScaleTuple):
    newImage = pg.transform.scale(image,(int(DISPLAYS[displayIndex][0]*(originalScaleTuple[0]/100)),
                                         int(DISPLAYS[displayIndex][1]*(originalScaleTuple[1]/100))))
    return newImage


def resizeDisplay():
    screen = pg.display.set_mode(DISPLAYS[displayIndex])
    icon.updateSize()


icon = Icon(100,100)
all_sprites = pg.sprite.Group()
arrow = Arrow(all_sprites)
pg.display.set_caption('GOTY 2025')
infoObject = pg.display.Info()

screen = pg.display.set_mode((infoObject.current_w, infoObject.current_h))
screen.fill((100, 100, 100))
pg.mouse.set_visible(False)
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == KEYDOWN:
            screen.fill((100, 100, 100))
            if event.key == K_LEFT:
                displayIndex -= 1
                if displayIndex < 0:
                    displayIndex = 5
                resizeDisplay()
            elif event.key == K_RIGHT:
                displayIndex += 1
                if displayIndex > 5:
                    displayIndex = 0
                resizeDisplay()
            if pg.mouse.get_focused():
                mouse_pos = event.pos
                all_sprites.update(mouse_pos)
                all_sprites.draw(screen)
            screen.blit(icon.image, (icon.rect.x, icon.rect.y))
            pg.display.update()

        elif event.type == pg.MOUSEMOTION:
            screen.fill((100, 100, 100))
            if pg.mouse.get_focused():
                mouse_pos = event.pos
                all_sprites.update(mouse_pos)
                all_sprites.draw(screen)
    pg.display.update()
