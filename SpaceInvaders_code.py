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
    def __init__(self, x, y, d, image, ):
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

    def shift_down(self):
        self.rect.y += (1/10) * self.d

    def update(self, direction):
        self.rect.x += direction * self.speed



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = -10
        self.image = shot
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += self.speed

# -------------- Functions ------------


def create_row(row, separation, img1):
    for e in range(num_aliens):
        row.add(Alien((e + 1) * d + e * 20, d * separation, d, img1))


def game_over():
    font_large = pygame.font.SysFont("Space Invaders Regular", 100)
    text2 = font_large.render("Game Over!", True, (255, 255, 255))
    screen.blit(text2, (80, height / 2 - 50))


# -------------- Main Game Loop ------------
direction = 1

num_shots = 0
shots = pygame.sprite.Group()
for i in range(num_shots):
    Bullet(player_x, 440)
    shots.add(i)

num_aliens = 11
d = 40

row_1 = pygame.sprite.Group()
create_row(row_1, 1.5, invader1)

row_2 = pygame.sprite.Group()
create_row(row_2, 2.5, invader2)

row_3 = pygame.sprite.Group()
create_row(row_3, 3.5, invader2)

row_4 = pygame.sprite.Group()
create_row(row_4, 4.5, invader3)

row_5 = pygame.sprite.Group()
create_row(row_5, 5.5, invader3)

all_aliens_list = pygame.sprite.Group()

all_aliens_list.add(row_1)
all_aliens_list.add(row_2)
all_aliens_list.add(row_3)
all_aliens_list.add(row_4)
all_aliens_list.add(row_5)

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
                shots.add(i)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] and player_x < width - 40:
        player_x += 5
    if keys[pygame.K_a] and player_x > 0:
        player_x -= 5

    #-----------Collisions-----------
    for bullet in shots:
        alien_hit_list = pygame.sprite.spritecollide(bullet, all_aliens_list, True)

        for alien in alien_hit_list:
            shots.remove(bullet)

        if bullet.rect.y < -10:
            shots.remove(bullet)
    for alien in all_aliens_list:
        bullet_hit_list = pygame.sprite.spritecollide(alien, shots, True)


    #-----------Alien Movement-----------
    for alien in all_aliens_list:
        if alien.rect.x + d >= width:
            direction = -1
            for i in all_aliens_list:
                i.shift_down()

        if alien.rect.x <= 0:
            direction = 1
            for i in all_aliens_list:
                i.shift_down()

    all_aliens_list.draw(screen)
    all_aliens_list.update(direction)
    shots.draw(screen)
    shots.update()

    screen.blit(player, (player_x, 550))
    pygame.display.update()