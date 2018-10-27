import pygame
import sys
import SQL
import random

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

invader2_2 = pygame.image.load('images/Enemy2_2.png')
invader2_2 = pygame.transform.scale(invader2_2, (34, 22))

invader3 = pygame.image.load('images/Enemy3.png')
invader3 = pygame.transform.scale(invader3, (32, 22))

invader3_2 = pygame.image.load('images/Enemy3_2.png')
invader3_2 = pygame.transform.scale(invader3_2, (32, 22))

shot = pygame.image.load("images/shot.png")

# -------------- Setting Events ------------
invader_move_event = pygame.USEREVENT + 1
invincible_event = pygame.USEREVENT + 2
player_respawn_event = pygame.USEREVENT + 3

# -------------- Global variables ------------
d = 40


# -------------- Classes -------------
class Player(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 550
        self.invincible = False
        self.respawning = False

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.rect.x < width - 40:
                self.rect.x += 5
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= 5


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, d, image1, image2, points):
        super().__init__()
        self.d = d
        # self.x_dir = 1
        self.img1 = image1
        self.img2 = image2
        self.image = image1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.points = points
        self.can_shoot = True

    def update(self, direction, update_speed, shift_down):

        self.rect.x += direction * update_speed

        if self.image == self.img1:
            self.image = self.img2

        elif self.image == self.img2:
            self.image = self.img1

        if shift_down:
            self.rect.y += 3 / 4 * self.d


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = -18
        self.image = shot
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.speed


class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = 5
        self.image = shot
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.speed


class TestBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = 5
        self.image = shot
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= self.speed


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect((x, y), (3, 3))
        self.rect.x = x
        self.rect.y = y
        # self.rect = self.image.get_rect()

    def update(self):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)


# -------------- Functions ------------


def game_over(score):
    print('game over')
    font = pygame.font.SysFont('Space Invaders Regular', 19)
    font_med = pygame.font.SysFont('Space Invaders Regular', 26)
    font_large = pygame.font.SysFont("Space Invaders Regular", 100)
    game_over_text = font_large.render("Game Over!", True, (255, 255, 255))
    add_score_text = font_med.render("Username:", True, (255, 255, 255))
    score_added_text = font_med.render("Score added to the leaderboard!", True, (255, 255, 255))

    input_box = pygame.Rect(300, 380, 140, 32)
    color_inactive = pygame.Color(255, 255, 255)
    color_active = pygame.Color(0, 255, 0, 70)
    color = color_inactive
    active = True
    text = ''
    name_entered = False
    score_added = False


    while True:
        pygame.display.update()
        clock.tick(15)
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            '''if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False'''

                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        name_entered = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif len(text) < 8:
                        text += event.unicode

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width

        if not name_entered:
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(screen, color, input_box, 2)
            screen.blit(add_score_text, (300, 350))
        if name_entered:
            screen.blit(score_added_text, (150, 350))
            if not score_added:
                SQL.add_score(text, score)
                SQL.display_table()
                print(SQL.scores)

                score_added = True

        y = 380

        if score_added:
            for line in SQL.scores:
                name_text = font.render(str(line[0]), True, (255, 255, 255))
                score_text = font.render(str(line[1]), True, (255, 255, 255))
                screen.blit(name_text, (200, y))
                screen.blit(score_text, (300, y))
                y += 20

            #screen.blit(score_text, (100, y))
    screen.blit(game_over_text, (100, 200))




def display_score(score):
    font = pygame.font.SysFont("Space Invaders Regular", 11)
    points = font.render("score= " + str(score), True, (255, 255, 255))
    screen.blit(points, (5, 5))


def display_lives(lives):
    font = pygame.font.SysFont("Space Invaders Regular", 11)
    render_lives = font.render("Lives:", True, (255, 255, 255))
    screen.blit(render_lives, (680, 7))
    player_small = pygame.transform.scale(player, (20, 15))

    if lives >= 1:
        screen.blit(player_small, (725, 5))

    if lives >= 2:
        screen.blit(player_small, (745, 5))

    if lives >= 3:
        screen.blit(player_small, (765, 5))


def create_row(row, y_separation, img1, img2, points):
    num_aliens = 11
    for e in range(num_aliens):
        row.add(Alien((e + 1) * d + e * 10, d * y_separation, d, img1, img2, points))
        all_aliens_list.add(Alien((e + 1) * d + e * 10, d * y_separation, d, img1, img2, points))


def reset():
    create_row(row_1, 1.5, invader1, invader1_2, 30)
    create_row(row_2, 2.5, invader2, invader2_2, 20)
    create_row(row_3, 3.5, invader2, invader2_2, 20)
    create_row(row_4, 4.5, invader3, invader3_2, 10)
    create_row(row_5, 5.5, invader3, invader3_2, 10)


def create_barrier(x_multiplier):
    rge = 10
    increment = 15
    y = 494
    for i in range(5):
        for i in range(rge):
            all_barriers.add(Barrier(i * 3 + x_multiplier + increment, y))
        rge += 2
        increment -= 3
        y += 3

    for i in range(6):
        for i in range(20):
            all_barriers.add(Barrier(i * 3 + x_multiplier, y))
        y += 3

    increment = 39
    rge = 7
    for i in range(3):
        for i in range(rge):
            all_barriers.add(Barrier(i * 3 + x_multiplier, y))
            all_barriers.add(Barrier(i * 3 + x_multiplier + increment, y))
        rge -= 1
        increment += 3
        y += 3


    for i in range(5):
        all_barriers.add(Barrier(i * 3 + x_multiplier, y))
        all_barriers.add(Barrier(i * 3 + x_multiplier + 45, y))


# -------------- Creating and setting groups ------------
shots = pygame.sprite.Group()

alien_shots = pygame.sprite.Group()
test_shots = pygame.sprite.Group()
all_aliens_list = pygame.sprite.Group()

row_1 = pygame.sprite.Group()
row_2 = pygame.sprite.Group()
row_3 = pygame.sprite.Group()
row_4 = pygame.sprite.Group()
row_5 = pygame.sprite.Group()
reset()

all_barriers = pygame.sprite.Group()

create_barrier(70)
create_barrier(250)
create_barrier(430)
create_barrier(610)


# -------------- Start screen loop------------

def start_screen():
    bx, by = 350, 150
    r, g, b = 255, 255, 255
    font = pygame.font.SysFont('Space Invaders Regular', 26)
    play = font.render("Play", True, (r, g, b))
    screen.blit(play, (bx, by))

    Space_ivaders = font.render("Space    Invaders", True, (255, 255, 255))
    screen.blit(Space_ivaders, (250, 200))

    font_small = pygame.font.SysFont('Space Invaders Regular', 19)

    screen.blit(font.render("*SCORE ADVANCE TABLE*", True, (255, 255, 255)), (180, 290))
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

            # Checking if the mouse cursor is withing the bounds of the button when clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] >= bx and pygame.mouse.get_pos()[1] >= by:
                    if pygame.mouse.get_pos()[0] <= bx + 77 and pygame.mouse.get_pos()[1] <= by + 27:
                        game_loop()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()


# --------------Main game loop------------

def game_loop():
    playing = True
    direction = 1
    speed = 560
    speed_prev = 561
    score = 0
    players = pygame.sprite.Group()
    players.add(Player(350))

    lives = 3

    aliens_prev = len(all_aliens_list)

    while playing:
        # Limits the loop to run 60 times per second (60fps)
        clock.tick(60)
        # resets the screen to black each time to allow the new image to be displayed over it
        screen.fill((0, 0, 0))

        # checks if the speed has changed and if it has, pass the new variable of speed into the event timer and
        # sets the previous speed to its new value
        if speed_prev != speed:
            pygame.time.set_timer(invader_move_event, speed)
            speed_prev = speed

        # if there aren't any players in the players list and the player still has lives, add a new player
        #
        if not players and lives > 0:
            players.add(Player(350))
            for player in players:
                player.invincible = True
                player.respawning = True

                pygame.time.set_timer(invincible_event, 1500)
                pygame.time.set_timer(player_respawn_event, 500)

        # end the game loop if the player is out of lives
        if lives == 0:
            playing = False

        # -----------Collisions-----------
        for bullet in shots:
            # for every bullet in the shots group, chack if it collides with anything in the all_aliens_list
            # if an alien is hit it is removed from the all_aliens list and added to alien_hit_list,
            # removing it from the screen
            alien_hit_list = pygame.sprite.spritecollide(bullet, all_aliens_list, True)

            # remove the bullet for each alien hit and increce the score by the individual aliens score value
            for alien in alien_hit_list:
                shots.remove(bullet)
                score += alien.points

            # remove the bullet if it goes off screen
            if bullet.rect.y < -10:
                shots.remove(bullet)

        # -----------Testing if an alien can shoot-----------
        # resets all the can_shoot values to true before check
        for alien in all_aliens_list:
            alien.can_shoot = True

        for bullet in test_shots:
            # tests if a bullet hits the alien
            test_hit_list = pygame.sprite.spritecollide(bullet, all_aliens_list, False)

            # removes any bullet that hits an alien
            for alien in test_hit_list:
                test_shots.remove(bullet)

            # if an alien is hit by a bullet that is coming from the alien below, it cannot shoot.
            # it then removes it from the list so if the alien below is destroyed and stops shooting
            # its not stuck in there unable to shoot for the rest of the game
            for alien in test_hit_list:
                alien.can_shoot = False
                test_hit_list.remove(alien)

        # removes the bullet if it goes too high
        for bullet in test_shots:
            if bullet.rect.y <= 50:
                test_shots.remove(bullet)

        # -----------Testing for player being shot-----------
        for bullet in alien_shots:
            for player in players:
                if not player.invincible:
                    player_hit_lsit = pygame.sprite.spritecollide(bullet, players, True)

            for i in player_hit_lsit:
                lives -= 1
                player_hit_lsit.remove(i)

            if bullet.rect.y > height:
                alien_shots.remove(bullet)

        # -----------Testing for barrier being shot-----------
        for bullet in shots:
            barrier_hit_list = pygame.sprite.spritecollide(bullet, all_barriers, True)

            for barrier in barrier_hit_list:
                alien_shots.remove(bullet)
                shots.remove(bullet)

        for bullet in alien_shots:
            barrier_hit_list = pygame.sprite.spritecollide(bullet, all_barriers, True)

            for barrier in barrier_hit_list:
                alien_shots.remove(bullet)

        # -----------Testing if a player bullet hits an alien bullet-----------
        for bullet in shots:
            alien_shots_hit_list = pygame.sprite.spritecollide(bullet, alien_shots, True)
            for i in alien_shots_hit_list:
                shots.remove(bullet)

        # -----------Alien Movement-----------

        shift_down = False
        for alien in all_aliens_list:
            if alien.rect.x + d >= width:
                direction = -1
                shift_down = True

            if alien.rect.x <= 0:
                direction = 1
                shift_down = True

            if alien.rect.y >= 494:
                playing = False

            # -----------Alien shooting-----------
            if pygame.time.get_ticks() % 500:
                test_shots.add(TestBullet(alien.rect[0] + 15, alien.rect[1] - 10))

            if alien.can_shoot:
                if pygame.time.get_ticks() % random.randint(10, 3000) == 0:
                    alien_shots.add(AlienBullet(alien.rect[0] + 15, alien.rect[1] + 30))

        if not all_aliens_list:
            speed = 560
            reset()
            aliens_prev = len(all_aliens_list)

        if len(all_aliens_list) < aliens_prev:
            speed -= 10
            aliens_prev = len(all_aliens_list)

        # -----------Event polling-----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for player in players:
                        if not shots:
                            shoot_x = player.rect.x + 18
                            shots.add(Bullet(shoot_x, 540))

            if event.type == invincible_event:
                for player in players:
                    player.invincible = False

            if event.type == player_respawn_event:
                for player in players:
                    player.respawning = False

            if event.type == invader_move_event:
                all_aliens_list.update(direction, 10, shift_down)

        all_aliens_list.draw(screen)
        shots.draw(screen)
        shots.update()
        test_shots.update()
        alien_shots.draw(screen)
        alien_shots.update()
        display_score(score)
        display_lives(lives)
        for player in players:
            if not player.respawning:
                players.draw(screen)
                players.update()
        all_barriers.update()
        pygame.display.update()

        if not playing:
            game_over(score)

start_screen()
