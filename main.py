import pygame
import os
import sys


pygame.init()
size = width, heigth = 800, 632
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Skateboard Breaker")


def load_image(name, colorkey=None):
    filename = os.path.join('data', name)
    if not os.path.isfile(filename):
        print(f"Не найдено: {filename}")
        sys.exit()
    image = pygame.image.load(filename)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = 'data' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, "."), level_map))


def generate_level():
    pass


class Ball(pygame.sprite.Sprite):
    image = load_image('ball_blue_small.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.vx = 1
        self.vy = 5

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, vertical_boards):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, horizontal_boards):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, player_group):
            self.vy = -self.vy


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites, balls)
        if x1 == x2:
            self.add(vertical_boards)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_boards)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, player_group)
        self.image = load_image('1.png')
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 600
        self.vx = 10

    def update(self, *args):
        if self.rect.left == left.rect.x:
            self.rect.x += 10
        if self.rect.right == right.rect.x:
            self.rect.x -= 10
        if args and args[0].key == pygame.K_LEFT:
            self.rect.x -= self.vx
        if args and args[0].key == pygame.K_RIGHT:
            self.rect.x += self.vx


all_sprites = pygame.sprite.Group()
vertical_boards = pygame.sprite.Group()
horizontal_boards = pygame.sprite.Group()
balls = pygame.sprite.Group()
# tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

left = Border(0, 0, 0, heigth)
right = Border(width, 0, width, heigth)
Border(0, 0, width, 0)
Border(0, heigth, width, heigth)
Ball()
player = Player()

clock = pygame.time.Clock()
fps = 60
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.update(event)
    if keys[pygame.K_RIGHT]:
        player.update(event)
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
