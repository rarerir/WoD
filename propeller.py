import sys
import pygame


class Circle(pygame.sprite.Sprite):
    def __init__(self, dx, dy,*group):
        super().__init__(*group)
        self.hp = 1
        self.color = (255, 0, 0)
        self.dx = dx
        self.dy = dy
        self.radius = 30
        self.add(boolets)
        self.x = 200
        self.y = 200
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        self.rect = self.rect.move(self.dx, self.dy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.dy = -self.dy
            self.hp -= 1
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.dx = -self.dx
            self.hp -= 1
        if self.hp < 0:
            self.kill()

    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


# Initialize Pygame
pygame.init()
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
boolets = pygame.sprite.Group()
size = width, height = 400, 400
Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)
screen = pygame.display.set_mode(size)
sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

Circle(4, 3, sprites)
Circle(-4, -3, sprites)
Circle(-3, 4, sprites)
Circle(3, -4, sprites)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    sprites.update()
    for sprite in sprites:
        sprite.draw()

    pygame.display.update()
    clock.tick(15)
