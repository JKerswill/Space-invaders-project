import pygame
import sys

# -------------- Initialization ------------
pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('images/game.png')
pygame.display.set_icon(icon)

# -------------- Setting Images ------------
player = pygame.image.load('images/ship.png')
player = pygame.transform.scale(player, (40, 30))
player_x = 350
player_top = screen.get_height() - player.get_height()
player_left = screen.get_width() / 2 - player.get_width() / 2

invader1 = pygame.image.load('images/Enemy1.png')
invader1 = pygame.transform.scale(invader1, (30, 22))
invader1_2 = pygame.image.load('images/Enemy1_2.png')
invader1_2 = pygame.transform.scale(invader1_2, (30, 22))
invader2 = pygame.image.load('images/Enemy2.png')
invader2 = pygame.transform.scale(invader2, (34, 22))
invader3 = pygame.image.load('images/Enemy3.png')
invader3 = pygame.transform.scale(invader3, (32, 22))

shot = pygame.image.load("images/shot.png")


# -------------- Classes -------------


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, d, image):
        super().__init__()
        self.d = d
        self.x_dir = 1
        self.speed = 1
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y, self.d, self.d))

    def move(self):
        self.rect.x += self.x_dir * self.speed

    def shift_down(self):
        self.rect.y += self.d


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.speed = -5
        self.image = shot
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        self.rect.y += self.speed


# -------------- Functions ------------


def create_row(row, separation, img1):
    for e in range(num_aliens):
        e = Alien((e + 1) * d + e * 20, d * separation, d, img1)
        row.append(e)


def movement(row):
    for alien in list(row):
        alien.draw()
        alien.move()

    for e in range(num_aliens):
        if row[e].rect.x + d >= width:
            for j in range(num_aliens):
                row[j].x_dir = -1
                row[j].shift_down()

    if row[0].rect.x <= 0:
        for j in range(num_aliens):
            row[j].x_dir = 1
            row[j].shift_down()


def game_over():
    font_large = pygame.font.SysFont("Space Invaders Regular", 100)
    text2 = font_large.render("Game Over!", True, (255, 255, 255))
    screen.blit(text2, (80, height / 2 - 50))


# -------------- Main Game Loop ------------

num_shots = 0
shots = []
for i in range(num_shots):
    Bullet(player_x, 440)
    shots.append(i)

num_aliens = 11
d = 40
# row_1 = []
# create_row(row_1, 1.5, invader1)
row_1 = pygame.sprite.Group()
for e in range(num_aliens):
    row_1.add(Alien((e + 1) * d + e * 20, d * 1.5, d, invader1))

row_2 = []
create_row(row_2, 2.5, invader2)

row_3 = []
create_row(row_3, 3.5, invader2)

row_4 = []
create_row(row_4, 4.5, invader3)

row_5 = []
create_row(row_5, 5.5, invader3)

while True:
    clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                num_shots += 1
                shoot_x = player_x + 18
                i = Bullet(shoot_x, 540)
                shots.append(i)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] and player_x < width - 40:
        player_x += 5
    if keys[pygame.K_a] and player_x > 0:
        player_x -= 5
    row_1.draw(screen)
    # movement(row_1)
    movement(row_2)
    movement(row_3)
    movement(row_4)
    movement(row_5)

    for alien in row_1:
        alien.draw()
        alien.move()

    for e in range(num_aliens):
        if row_1.sprites()[e].rect.x + d >= width:
            for j in range(num_aliens):
                row_1.sprites()[j].x_dir = -1
                row_1.sprites()[j].shift_down()

        if row_1.sprites()[0].rect.x <= 0:
            for j in range(num_aliens):
                row_1.sprites()[j].x_dir = 1
                row_1.sprites()[j].shift_down()

    for i in range(num_shots):
        shots[i].draw()
        shots[i].move()

    screen.blit(player, (player_x, 550))
    pygame.display.update()
