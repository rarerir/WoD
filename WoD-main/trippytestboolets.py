import sys
import random
import pygame


class Circle(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.color = (255, 0, 0)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.radius = 2
        self.add(boolets)
        self.x = random.randint(self.radius, width - self.radius)
        self.y = random.randint(self.radius, height - self.radius)
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        self.rect = self.rect.move(self.dx, self.dy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.dy = -self.dy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.dx = -self.dx
        colided = pygame.sprite.spritecollideany(self, boolets)
        if colided != self:
            colided.explode()
            self.explode()

    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def explode(self):
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
        self.kill()


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
size = width, height = 900, 900
Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)
screen = pygame.display.set_mode(size)
sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

# Create circles
for i in range(10):
    Circle(sprites)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    sprites.update()
    for sprite in sprites:
        sprite.draw()

    pygame.display.update()
    clock.tick(60)
