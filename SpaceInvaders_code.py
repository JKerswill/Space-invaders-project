import pygame
import sys
import SQL

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

invader1 = pygame.image.load('images/Enemy1.png')
invader1 = pygame.transform.scale(invader1, (30, 22))
invader1_2 = pygame.image.load('images/Enemy1_2.png')
invader1_2 = pygame.transform.scale(invader1_2, (30, 22))
invader2 = pygame.image.load('images/Enemy2.png')
invader2 = pygame.transform.scale(invader2, (34, 22))
invader3 = pygame.image.load('images/Enemy3.png')
invader3 = pygame.transform.scale(invader3, (32, 22))

shot = pygame.image.load("images/shot.png")

# -------------- Global variables ------------
d = 40



# -------------- Classes -------------


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, d, image, points):
        super().__init__()
        self.d = d
        #self.x_dir = 1
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.points = points

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y, self.d, self.d))

    def update(self, direction, update_speed, shift_down):

        self.rect.x += direction * update_speed

        if shift_down:
            self.rect.y += (1/2)*self.d



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

class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.draw.rect(screen, (0,255,0),(x, y, 3, 3))
        #self.rect = self.image.get_rect()

    def update(self):
        screen.blit(self.image)

# -------------- Functions ------------


def create_row(row, separation, img1, points):
    num_aliens = 11
    for e in range(num_aliens):
        row.add(Alien((e + 1) * d + e * 20, d * separation, d, img1, points))
        all_aliens_list.add(Alien((e + 1) * d + e * 20, d * separation, d, img1, points))

def game_over():
    print('game over')
    font_large = pygame.font.SysFont("Space Invaders Regular", 100)
    text2 = font_large.render("Game Over!", True, (255, 255, 255))
    screen.blit(text2, (150, 200))


def display_score(score):
    font = pygame.font.SysFont("", 16)
    points = font.render("score= "+str(score), True, (255, 255,255))
    screen.blit(points, (5, 5))

def reset():
    create_row(row_1, 1.5, invader1, 30)
    create_row(row_2, 2.5, invader2, 20)
    create_row(row_3, 3.5, invader2, 20)
    create_row(row_4, 4.5, invader3, 10)
    create_row(row_5, 5.5, invader3, 10)




# -------------- Main Game Loop ------------

num_shots = 0
shots = pygame.sprite.Group()
for i in range(num_shots):
    Bullet(player_x, 440)
    shots.add(i)



all_aliens_list = pygame.sprite.Group()

row_1 = pygame.sprite.Group()
row_2 = pygame.sprite.Group()
row_3 = pygame.sprite.Group()
row_4 = pygame.sprite.Group()
row_5 = pygame.sprite.Group()
reset()

def start_screen():
    bx, by = 350, 150
    R, G, B = 255, 255, 255
    start_button = pygame.draw.rect(screen, (0, 0, 0), (bx, by, 77, 27))
    font = pygame.font.SysFont('Space Invaders Regular', 26)
    play = font.render("Play", True, (R, G, B))
    screen.blit(play, (bx, by))


    Space_ivaders = font.render("Space    Invaders", True, (255, 255, 255))
    screen.blit(Space_ivaders, (250, 200))

    font_small = pygame.font.SysFont('Space Invaders Regular', 19)

    screen.blit(font.render("*SCORE ADVANCE TABLE*", True, (255, 255, 255)), (180 ,290))
    screen.blit(invader1, (250, 347))
    screen.blit(font_small.render("= 30       points", True, (255, 255, 255)), (287, 350))
    screen.blit(invader2, (250, 387))
    screen.blit(font_small.render("= 20       points", True, (255, 255, 255)), (287, 390))
    screen.blit(invader3, (250, 427))
    screen.blit(font_small.render("= 10        points", True, (0, 255, 0)), (287, 430))



    while True:
        pygame.display.update()
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()



            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] >= bx and pygame.mouse.get_pos()[1] >= by:
                    if pygame.mouse.get_pos()[0] <= bx + 77 and pygame.mouse.get_pos()[1] <= by + 27:
                        game_loop(num_shots)




def game_loop(num_shots):
    playing = True
    player_x = 350
    direction = 1
    speed = 10
    score = 0


    while playing:
        clock.tick(60)
        screen.fill((0, 0, 0))

        # -----------Register keypress-----------
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
            player_x += 10
        if keys[pygame.K_a] and player_x > 0:
            player_x -= 10

        #-----------Collisions-----------
        for bullet in shots:
            alien_hit_list = pygame.sprite.spritecollide(bullet, all_aliens_list, True)

            for alien in alien_hit_list:
                shots.remove(bullet)
                score += alien.points


            if bullet.rect.y < -10:
                shots.remove(bullet)



        #-----------Alien Movement-----------

        shift_down = False
        accelerate = False
        for alien in all_aliens_list:
            if alien.rect.x + d >= width:
                direction = -1
                shift_down = True
                accelerate = True

            if alien.rect.x <= 0:
                direction = 1
                shift_down = True
                accelerate = True

            #print(alien.rect.y)

            if alien.rect.y >= 521:
                playing = False


        #if accelerate and speed != 4:
            #speed += 5





        if not all_aliens_list:
            #speed -= 1
            reset()

        all_aliens_list.draw(screen)
        all_aliens_list.update(direction, speed/10, shift_down)
        shift_down = False
        shots.draw(screen)
        shots.update()
        display_score(score)
        screen.blit(player, (player_x, 550))
        pygame.display.update()

        if not playing:
            SQL.add_score('jamie', score)
            SQL.display_table()
            game_over()


start_screen()


