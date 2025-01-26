import pygame
import os
import sys

pygame.init()
size = width, heigth = 800, 632
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Skateboard Breaker")

all_sprites = pygame.sprite.Group()
vertical_boards = pygame.sprite.Group()
horizontal_boards = pygame.sprite.Group()
balls = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
bonus_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

TIMER_EVENT = 30
MILLIS = 10 * 1000
clock = pygame.time.Clock()
FPS = 60


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
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, "."), level_map))


class Ball(pygame.sprite.Sprite):
    image = load_image('ball_blue_small.png')

    def __init__(self):
        super().__init__(all_sprites, balls)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300
        self.vx = 3
        self.vy = 3

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect.bottom > heigth:
            self.kill()
        if pygame.sprite.spritecollideany(self, vertical_boards):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, horizontal_boards):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, player_group):
            self.vx = -self.vx
            if player.rect.top < self.rect.bottom < player.rect.bottom:
                self.vy = -self.vy
            if player.rect.right > self.rect.right > player.rect.left:
                self.vx = -self.vx
        if pygame.sprite.spritecollide(self, tiles_group, True):
            for block in tiles_group:
                if block.rect.top < self.rect.top < block.rect.bottom \
                        or block.rect.top < self.rect.bottom < block.rect.bottom:
                    self.vy = -self.vy
                if block.rect.left < self.rect.right < block.rect.right \
                        or block.rect.right < self.rect.left < block.rect.left:
                    self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
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
        self.rect.y = 595
        self.vx = 5

    def update(self, *args):
        if self.rect.left == left.rect.x:
            self.rect.x += 10
        if self.rect.right == right.rect.x:
            self.rect.x -= 10
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.vx
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.vx


class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, bonus_group)
        self.bonus_img = ['лайтер.jpg', 'лайтер.jpg']
        self.image = load_image(self.bonus_img[0])
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 400
        self.v = 3

    def update(self):
        self.rect = self.rect.move(0, self.v)
        if self.rect.top > heigth:
            self.kill()
        if pygame.sprite.spritecollideany(self, player_group):
            self.kill()
            if self.bonus_img[0] == 'лайтер.jpg':
                for i in range(2):
                    Ball()
            # if self.bonus_img[0] == 'лайтер.jpg':
            # for ball in balls:
            #     pygame.transform.scale(ball.image, (50, 50))


class Tile(pygame.sprite.Sprite):
    image = load_image('block.png')

    def __init__(self, x, y):
        super().__init__(all_sprites, tiles_group)
        self.image = Tile.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            tile = level[y][x]
            if tile == '#':
                Tile(x * 40, y * 40)


def start_screen():
    fon = load_image('start.png')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.blit(fon, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


left = Border(0, 0, 0, heigth)
right = Border(width, 0, width, heigth)
Border(0, 0, width, 0)
Ball()
player = Player()
pygame.time.set_timer(TIMER_EVENT, MILLIS)

start_screen()
generate_level(load_level('level_1.txt'))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == TIMER_EVENT:
            Bonus()
    if len(balls) == 0:
        print("Вы проиграли")
        generate_level(load_level('level_2.txt'))
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update()
    player.update()
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
