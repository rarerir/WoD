import pygame as pg

pg.init()

WIDTH, HEIGHT = 800, 600

clock = pg.time.Clock()
window = pg.display.set_mode((WIDTH, HEIGHT))
objects = pg.sprite.Group()


class Vec2:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __iter__(self):
        return iter((self.x, self.y))


class Square(pg.sprite.Sprite):
    def __init__(self, pos=Vec2(), size=50):
        """
        Создает объект-квадарат square
        :param pos: Позиция квадрата!!!!
        :param size: Размер стороны квадратнак
        """
        super().__init__()
        self.add(objects)
        self.pos = pos
        self.size = size
        self.rect = self.update_rect()

    def update_rect(self):
        return pg.Rect(*self.pos, self.size, self.size)

    def set(self, x=0, y=0, size=0):
        self.pos.x = x if x != 0 else self.pos.x
        self.pos.y = y if y != 0 else self.pos.y
        self.size = size if size != 0 else self.size
        self.rect = self.update_rect()

    def draw(self):
        pg.draw.rect(window, "white", self.rect)

    def collideany(self):
        self.remove(objects)
        _any = pg.sprite.spritecollideany(self, objects)
        self.add(objects)
        return _any


def quit_hander():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()


speed = 1
s1 = Square(Vec2(0, 50), 50)
s2 = Square(Vec2(100, 50), 50)
s3 = Square(Vec2(WIDTH - 50, 50), 50)


def key_handler():
    pass


def main():

    global speed
    s1.draw()
    s2.draw()
    s2.set(x=s2.pos.x + speed)
    s3.draw()
    if s2.collideany():
        speed *= -1


while True:
    quit_hander()
    key_handler()
    window.fill("black")
    main()
    pg.display.update([0, 0, 250, 250])
    pg.display.flip()
    clock.tick(120)
