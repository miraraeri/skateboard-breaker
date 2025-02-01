import pygame
import os
import sys
from random import randrange

pygame.init()
size = width, heigth = 800, 632
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Skateboard Breaker")

fon_music = "Love in Mexico - Carmen María and Edu Espinal.mp3"
pygame.mixer.music.load(f"data/{fon_music}")
pygame.mixer.music.play(-1)
bonus_sound = pygame.mixer.Sound('data/bonus_music.mp3')
collide_music = pygame.mixer.Sound('data/collide_music.mp3')
gameover_music = pygame.mixer.Sound('data/game_over_music.mp3')
victory_music = pygame.mixer.Sound('data/victory_music.mp3')

all_sprites = pygame.sprite.Group()
vertical_boards = pygame.sprite.Group()
horizontal_boards = pygame.sprite.Group()
balls = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
bonus_group = pygame.sprite.Group()
bonus_time_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

TIMER_EVENT = 30
MILLIS = 10000
BONUS_DURATION = 500000
clock = pygame.time.Clock()
FPS = 60
lives = 3
gameover = False
gmov_music = False
win = False
win_music = False
level_num = 1


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
    image = load_image('ball.png')

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
            if player.rect.top < self.rect.bottom < player.rect.bottom:
                self.vy = -self.vy
            if player.rect.right > self.rect.right > player.rect.left:
                self.vx = -self.vx
        if pygame.sprite.spritecollide(self, tiles_group, True):
            collide_music.play()
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
        self.image = load_image('skate.png')
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 590
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
        super().__init__(all_sprites, bonus_group, bonus_time_group)
        self.bonus_img = ['more balls.png', 'big ball.png', 'long sk.png']
        self.type_image = self.bonus_img[randrange(0, len(self.bonus_img))]
        self.image = load_image(self.type_image)
        self.rect = self.image.get_rect()
        self.rect.x = randrange(0, 760)
        self.rect.y = 100
        self.v = 3
        self.active = False
        self.time_left = BONUS_DURATION
        self.type = ''

    def update(self):
        self.rect = self.rect.move(0, self.v)
        if self.rect.top > heigth:
            self.kill()
        if pygame.sprite.spritecollideany(self, player_group):
            bonus_sound.play()
            self.apply_bonus()
            self.remove(bonus_group, all_sprites)
            self.active = True

    def apply_bonus(self):
        global lives
        if self.type_image == self.bonus_img[0]:
            self.type = 'count'
            for i in range(2):
                Ball()
        if self.type_image == self.bonus_img[1]:
            self.type = 'ball_size'
            for ball in balls:
                ball.image = pygame.transform.scale(ball.image, (50, 50))
                ball.rect = ball.image.get_rect(topleft=ball.rect.topleft)
            self.time_left = BONUS_DURATION
        if self.type_image == self.bonus_img[2]:
            self.type = 'skateboard_size'
            player.image = pygame.transform.scale(player.image, (100, 32))
            player.rect = player.image.get_rect(topleft=player.rect.topleft)
            self.time_left = BONUS_DURATION
        # if self.bonus_img[0]:
        #     lives = lives + 1
        #     print(lives)

    def update_bonus(self):
        if self.active:
            self.time_left -= 1000
            if self.time_left <= 0:
                self.deactivate()

    def deactivate(self):
        self.active = False
        if self.type == 'ball_size':
            for ball in balls:
                ball.image = pygame.transform.scale(ball.image, (20, 20))
                ball.rect = ball.image.get_rect(topleft=ball.rect.topleft)
        if self.type == 'skateboard_size':
            player.image = pygame.transform.scale(player.image, (80, 32))
            player.rect = player.image.get_rect(topleft=player.rect.topleft)


class Tile(pygame.sprite.Sprite):
    image = load_image('block.jpg')

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


def game_over():
    global gmov_music
    if not gmov_music:
        gameover_music.play()
        gmov_music = True
    pygame.mixer.music.pause()
    fon = load_image('over.jpg')
    screen.blit(fon, (0, 0))
    pygame.display.flip()


def lose_life():
    global lives, balls, gameover
    lives -= 1
    if lives <= 0:
        gameover = True
    else:
        balls.empty()
        Ball()


def restart_game():
    global all_sprites, player_group, tiles_group, balls, lives, gameover, gmov_music
    all_sprites.empty()
    player_group.empty()
    balls.empty()
    tiles_group.empty()

    Ball()
    Player()

    lives = 3
    generate_level(load_level(f'level_{level_num}.txt'))
    gameover = False
    gmov_music = False
    pygame.mixer.music.unpause()


def next_level():
    global level_num, win
    level_num += 1
    if level_num > 2:
        win = True
        return
    restart_game()


def win_screen():
    global level_num, win, win_music
    fon = load_image("start.jpg")
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    pygame.mixer.music.pause()
    if not win_music:
        victory_music.play()
        win_music = True
    if mouse[0]:
        win = False
        win_music = False
        level_num = 1
        restart_game()


left = Border(0, 0, 0, heigth)
right = Border(width, 0, width, heigth)
Border(0, 0, width, 0)
Ball()
player = Player()
pygame.time.set_timer(TIMER_EVENT, MILLIS)

start_screen()
generate_level(load_level(f'level_{level_num}.txt'))
game_fon = load_image('fon1.png')
my_event = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == TIMER_EVENT:
            Bonus()
    for bonus in bonus_time_group:
        bonus.update_bonus()
    mouse = pygame.mouse.get_pressed()
    if lives <= 0 and mouse[2]:
        restart_game()
    if len(tiles_group) == 0:
        next_level()
    if len(balls) == 0:
        lose_life()

    if not gameover and not win:
        screen.fill((255, 255, 255))
        screen.blit(game_fon, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
    elif gameover:
        game_over()
    elif win:
        win_screen()
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
