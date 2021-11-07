# game instructions for Windows

# Yellow Player
# UP, DOWN, LEFT, RIGHT TO MOVE
# RCTRL TO SHOOT
# . TO TURN AROUND

# Red Player
# W, S, A, D TO MOVE
# CAPS LOCK TO SHOOT
# TAB TO TURN AROUND

# Shoot the correct meteor = 10 point
# Shoot the wrong meteor = -5 points

# Shoot a correct asteroid = 5 points
# Shoot the wrong meteor = -5 points

# Shoot opposing player: they lose 5 point

import pygame
import random
from GameFiles import math_problems, true_statements, false_statements

pygame.font.init()
pygame.mixer.init()

pygame.init()

# fonts

LIVES_FONT = pygame.font.SysFont('rockwell', 25)
TIME_REMAINING_FONT = pygame.font.SysFont('rockwell', 25)
WINNER_FONT = pygame.font.SysFont('stencil', 100)
NUMBER_FONT = pygame.font.SysFont('stencil', 25)
QUESTION_FONT = pygame.font.SysFont('centuryschoolbook', 60)
INTRO_FONT = pygame.font.SysFont('centuryschoolbook', 40)
ASTEROID_FONT = pygame.font.SysFont('rockwell', 16)

# screen dimensions

WIDTH, HEIGHT = 900, 700

# character dimensions

SPACESHIP_WIDTH = 60
SPACESHIP_HEIGHT = 50

METEOR_WIDTH = 80
METEOR_HEIGHT = 80

ASTEROID_WIDTH = 220
ASTEROID_HEIGHT = 220

# to split game field in half

SEPARATOR_WIDTH = 10

# RBG colours

LIGHT_GREY = (217, 217, 217)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (153, 38, 0)
YELLOW = (204, 204, 0)
NAVY = (0, 0, 102)

# Gaps for upper display

TOP_DISPLAY_OUTER = 100
TOP_DISPLAY_GAP = 12

# frame speed and object velocities

FPS = 60

PLAYER_VEL = 4
BULLET_VEL = 5

METEOR_VEL = 1
ASTEROID_VEL = 0.5

MAX_BULLETS = 5

# load and scale images

# space image

SPACE = pygame.image.load('space.png')
SPACE_SCALED = pygame.transform.scale(SPACE, (WIDTH, HEIGHT - TOP_DISPLAY_OUTER))
SPACE_FOR_MENU = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))

# space ships

YELLOW_SHIP = pygame.image.load('spaceship_yellow.png')
YELLOW_SHIP_EAST = pygame.transform.rotate(pygame.transform.scale
                                           (YELLOW_SHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
YELLOW_SHIP_WEST = pygame.transform.rotate(pygame.transform.scale
                                           (YELLOW_SHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SHIP = pygame.image.load('spaceship_red.png')
RED_SHIP_EAST = pygame.transform.rotate(pygame.transform.scale(RED_SHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SHIP_WEST = pygame.transform.rotate(pygame.transform.scale(RED_SHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# lasers

YELLOW_LASER = pygame.image.load('pixel_laser_yellow.png')
RED_LASER = pygame.image.load('pixel_laser_red.png')
YELLOW_LASER_ROTATED = pygame.transform.rotate(YELLOW_LASER, 90)
RED_LASER_ROTATED = pygame.transform.rotate(RED_LASER, 90)

# meteor images

METEOR_ONE = pygame.image.load('meteor (2).png')
METEOR_ONE_SCALED = pygame.transform.scale(METEOR_ONE, (METEOR_WIDTH, METEOR_HEIGHT))

METEOR_TWO = pygame.image.load('meteor (2).png')
METEOR_TWO_SCALED = pygame.transform.rotate(pygame.transform.scale(METEOR_ONE, (METEOR_WIDTH, METEOR_HEIGHT)), 90)

METEOR_THREE = pygame.image.load('meteor (2).png')
METEOR_THREE_SCALED = pygame.transform.rotate(pygame.transform.scale(METEOR_ONE, (METEOR_WIDTH, METEOR_HEIGHT)), 180)

METEOR_FOUR = pygame.image.load('meteor (2).png')
METEOR_FOUR_SCALED = pygame.transform.rotate(pygame.transform.scale(METEOR_ONE, (METEOR_WIDTH, METEOR_HEIGHT)), 270)

# asteroid image
ASTEROID = pygame.image.load('asteroid.png')
ASTEROID_SCALED = pygame.transform.scale(ASTEROID, (ASTEROID_WIDTH, ASTEROID_HEIGHT))

# system window

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE CONQUEST")


class Laser:
    def __init__(self, x, y, img, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.img = img
        self.mask = pygame.mask.from_surface(img)

    def move_laser(self, vel):
        self.x += vel

    def draw_laser(self):
        WIN.blit(self.img, (self.x, self.y))

    def check_if_laser_on_screen(self):
        if 0 < self.x < WIDTH and TOP_DISPLAY_OUTER < self.y < HEIGHT:
            return True
        else:
            return False


class Player:
    COOL_DOWN = 30

    def __init__(self, x, y, images, orientation, health=50):
        self.x = x
        self.y = y
        self.east, self.west = images
        self.orientation = orientation  # there are 2 directions for the players - east and west
        self.health = health
        self.lasers = []
        self.mask = pygame.mask.from_surface(self.east)
        self.mask = pygame.mask.from_surface(self.west)
        self.cool_down_counter = 0

    def draw_player(self, window):
        if self.orientation == 'east':
            window.blit(self.east, (self.x, self.y))
        else:
            window.blit(self.west, (self.x, self.y))

        for laser in self.lasers:
            laser.draw_laser()

    # cool down ensure a half second break between shots

    def cool_down(self):
        if self.cool_down_counter >= self.COOL_DOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self, x, y, img):
        if self.cool_down_counter == 0:
            laser = Laser(x, y, img, self.orientation)
            self.lasers.append(laser)
            gun_fire = pygame.mixer.Sound('Assets_Gun+Silencer.mp3')
            gun_fire.play()
            self.cool_down_counter = 1

    def get_width(self):
        return self.west.get_width()

    def get_height(self):
        return self.west.get_height()

    def move_lasers(self, vel):

        for laser in self.lasers:
            if laser.direction == 'east':
                laser.x += vel
            elif laser.direction == 'west':
                laser.x -= vel


class Meteor:
    def __init__(self, x, y, img, answer):
        self.x = x
        self.y = y
        self.img = img
        self.answer = answer
        self.mask = pygame.mask.from_surface(self.img)

    def draw_meteor(self):
        WIN.blit(self.img, (self.x, self.y))

    def move_meteor(self, vel):
        self.x += vel
        self.y += vel

    def check_if_on_screen(self):
        if 0 - self.img.get_width() < self.x < WIDTH and self.y < HEIGHT:
            return True
        else:
            return False


class MeteorOne(Meteor):
    def __init__(self, x, y, img, number, answer):
        super().__init__(x, y, img, answer)
        self.number = number

    def draw_meteor(self):
        number = NUMBER_FONT.render(str(self.number), True, WHITE)
        WIN.blit(self.img, (self.x, self.y))
        WIN.blit(number, (self.x + self.img.get_width() / 2 - number.get_width() - 5,
                          self.y + self.img.get_height() / 2 - number.get_height() / 2 + 5))

    def move_meteor(self, vel):
        self.x -= 1
        self.y += 1


class MeteorTwo(Meteor):
    def __init__(self, x, y, img, number, answer):
        super().__init__(x, y, img, answer)
        self.number = number

    def draw_meteor(self):
        number = NUMBER_FONT.render(str(self.number), True, WHITE)
        WIN.blit(self.img, (self.x, self.y))
        WIN.blit(number, (self.x + self.img.get_width() / 2 - 13,
                          self.y + self.img.get_height() / 2 + 5))


class MeteorThree(Meteor):
    def __init__(self, x, y, img, number, answer):
        super().__init__(x, y, img, answer)
        self.number = number

    def draw_meteor(self):
        number = NUMBER_FONT.render(str(self.number), True, WHITE)
        WIN.blit(self.img, (self.x, self.y))
        WIN.blit(number, (self.x + self.img.get_width() / 2 - number.get_width() / 2 + 5,
                          self.y + self.img.get_height() / 2 - number.get_height() / 2 + 2))

    def move_meteor(self, vel):
        self.x += 1
        self.y -= 1

    def check_if_on_screen(self):
        if 0 - self.img.get_width() < self.x < WIDTH and self.y > TOP_DISPLAY_OUTER:
            return True
        else:
            return False


class MeteorFour(Meteor):
    def __init__(self, x, y, img, number, answer):
        super().__init__(x, y, img, answer)
        self.number = number

    def draw_meteor(self):
        number = NUMBER_FONT.render(str(self.number), True, WHITE)
        WIN.blit(self.img, (self.x, self.y))
        WIN.blit(number, (self.x + self.img.get_width() / 2 - number.get_width() / 2 - 5,
                          self.y + self.img.get_height() / 2 - number.get_height() / 2 - 10))

    def move_meteor(self, vel):
        self.x -= 1
        self.y -= 1

    def check_if_on_screen(self):
        if 0 - self.img.get_width() < self.x < WIDTH and self.y > TOP_DISPLAY_OUTER:
            return True
        else:
            return False


class Asteroid:
    def __init__(self, x, y, img, vel, text, correct):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.text = text
        self.correct = correct
        self.lives = 3
        self.mask = pygame.mask.from_surface(self.img)

    def draw_asteroid(self):
        problem = ASTEROID_FONT.render(str(self.text), True, WHITE)
        WIN.blit(self.img, (self.x, self.y))
        WIN.blit(problem, (self.x + self.img.get_width() / 2 - problem.get_width() / 2,
                           self.y + self.img.get_height() / 2 - problem.get_height() / 2))

    def move_asteroid(self):
        self.y += self.vel

    def lower_check_if_on_screen(self):
        if 0 - self.img.get_width() < self.x < WIDTH and self.y < HEIGHT:
            return True
        else:
            return False

    def upper_check_if_on_screen(self):
        if 0 - self.img.get_width() < self.x < WIDTH and self.y + self.img.get_width() > TOP_DISPLAY_OUTER:
            return True
        else:
            return False

    def get_width(self):
        return self.get_width()

    def get_height(self):
        return self.get_height()


def draw_window(yellow, red, win, up_meteors, low_meteors, up_asteroids,
                low_asteroids, question, secs_left, winner):

    # draw space background and separator

    WIN.blit(SPACE_SCALED, (0, TOP_DISPLAY_OUTER))
    pygame.draw.rect(win, GREY, (WIDTH / 2 - SEPARATOR_WIDTH / 2, 0, SEPARATOR_WIDTH, HEIGHT))

    # add players' health text

    red_health_score = LIVES_FONT.render("Red Health: " + str(red.health), True, WHITE)
    win.blit(red_health_score, (WIDTH - red_health_score.get_width() - 20, TOP_DISPLAY_OUTER + 20))

    yellow_health_score = LIVES_FONT.render("Yellow Health: " + str(yellow.health), True, WHITE)
    win.blit(yellow_health_score, (20, TOP_DISPLAY_OUTER + 20))

    # add seconds remaining text

    time_text = TIME_REMAINING_FONT.render("Time: " + str(secs_left), True, WHITE)
    win.blit(time_text, (WIDTH / 2 - time_text.get_width() / 2, HEIGHT - time_text.get_height() - 20))

    # draw meteors

    for meteor in up_meteors:
        meteor.draw_meteor()

    for meteor in low_meteors:
        meteor.draw_meteor()

    # draw asteroids

    for asteroid in up_asteroids:
        asteroid.draw_asteroid()

    for asteroid in low_asteroids:
        asteroid.draw_asteroid()

    # draw a display frame on top of the screen

    pygame.draw.rect(WIN, GREY, (0, 0, WIDTH, TOP_DISPLAY_OUTER))
    pygame.draw.rect(WIN, LIGHT_GREY, (TOP_DISPLAY_GAP, TOP_DISPLAY_GAP,
                                       WIDTH - 2 * TOP_DISPLAY_GAP, TOP_DISPLAY_OUTER - 2 * TOP_DISPLAY_GAP))

    # draw on the current question, asked to users

    question_text = QUESTION_FONT.render(question, True, NAVY)
    win.blit(question_text, (WIDTH / 2 - question_text.get_width() / 2,
                             TOP_DISPLAY_OUTER / 2 - question_text.get_height() / 2))

    # draw line separaring space background and the upper frame

    pygame.draw.rect(WIN, BLACK, (0, TOP_DISPLAY_OUTER, WIDTH, 5))

    # draw players

    red.draw_player(win)
    yellow.draw_player(win)

    # check for winner

    if winner is not None:
        display_winner(win, winner)

    pygame.display.update()


def handle_player_movements(keys, yellow, red):
    if keys[pygame.K_w] and yellow.y - PLAYER_VEL > 0 + TOP_DISPLAY_OUTER:
        yellow.y -= PLAYER_VEL
    if keys[pygame.K_UP] and red.y - PLAYER_VEL > 0 + TOP_DISPLAY_OUTER:
        red.y -= PLAYER_VEL
    if keys[pygame.K_s] and yellow.y + yellow.get_height() < HEIGHT:
        yellow.y += PLAYER_VEL
    if keys[pygame.K_DOWN] and red.y + red.get_height() < HEIGHT:
        red.y += PLAYER_VEL
    if keys[pygame.K_a] and yellow.x - PLAYER_VEL > 0:
        yellow.x -= PLAYER_VEL
    if keys[pygame.K_LEFT] and red.x + PLAYER_VEL > WIDTH / 2:
        red.x -= PLAYER_VEL
    if keys[pygame.K_d] and yellow.x + yellow.get_width() < WIDTH / 2:
        yellow.x += PLAYER_VEL
    if keys[pygame.K_RIGHT] and red.x + red.get_width() < WIDTH:
        red.x += PLAYER_VEL


# add function to handle all collision between players and/ or meteors


def collide(object1, object2):
    offset_x = int(object2.x) - int(object1.x)
    offset_y = int(object2.y) - int(object1.y)
    return object1.mask.overlap(object2.mask, (offset_x, offset_y)) is not None


def check_if_loser(yellow, red):
    if yellow.health <= 0:
        return 'Red Wins!'  # as winner

    elif red.health <= 0:
        return 'Yellow Wins!'  # as winner

    else:
        return None


def display_winner(win, winner):
    if winner == "Yellow Wins!":
        colour = YELLOW
    elif winner == 'Red Wins!':
        colour = RED
    else:
        colour = WHITE

    winning_text = WINNER_FONT.render(winner, True, colour)
    win.blit(winning_text, (WIDTH / 2 - winning_text.get_width() / 2,
                            HEIGHT / 2 - winning_text.get_height() / 2
                            + TOP_DISPLAY_OUTER / 2))


def main():
    yellow_images = (YELLOW_SHIP_EAST, YELLOW_SHIP_WEST)
    red_images = (RED_SHIP_EAST, RED_SHIP_WEST)

    winner = None
    question = ''

    # create and instance of players

    yellow = Player(150, 400, yellow_images, 'east')
    red = Player(700, 300, red_images, 'west')

    # list of bullets for each player

    yellow_bullets = []
    red_bullets = []

    # lists of meteors coming from the top and the bottom of the screen

    upper_meteors = []
    lower_meteors = []

    # lists of asteroids coming from the top and the bottom of the screen
    # max two asteroids on screen at one time

    upper_asteroids = []
    lower_asteroids = []

    # add music track

    pygame.mixer.music.load('space_odd.ogg')
    pygame.mixer.music.play(-1)

    run = True
    clock = pygame.time.Clock()

    # these variables will create a countdown in seconds, measured against the FPS

    seconds_remaining = 150
    fps_countdown = 0

    # these variables will help to pause the game after a player loses

    lost = False
    lost_count = 0

    while run:

        clock.tick(FPS)

        draw_window(yellow, red, WIN, upper_meteors, lower_meteors, upper_asteroids,
                    lower_asteroids, question, seconds_remaining, winner)

        # handles pausing the game for 3 seconds after player wins - then exits to main menu

        if lost:
            if lost_count > FPS * 4:
                run = False
            else:
                lost_count += 1
                continue

        # every time 'while' loop goes around 60 times,
        # the seconds remaining will reduce by 1

        if fps_countdown >= 60:
            seconds_remaining -= 1
            fps_countdown = 0

        elif fps_countdown < 60:
            fps_countdown += 1

        # handle game events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_TAB:
                    if yellow.orientation == 'east':
                        yellow.orientation = 'west'
                    else:
                        yellow.orientation = 'east'

                if event.key == pygame.K_PERIOD:
                    if red.orientation == 'east':
                        red.orientation = 'west'
                    else:
                        red.orientation = 'east'

                if event.key == pygame.K_RCTRL and red.orientation == 'east':
                    bullet = pygame.Rect(red.x, red.y - 20, 10, 5)
                    red_bullets.append(bullet)
                    red.shoot(bullet.x, bullet.y, RED_LASER_ROTATED)

                if event.key == pygame.K_RCTRL and red.orientation == 'west':
                    bullet = pygame.Rect(red.x - red.get_width() / 2 - 10, red.y - 20, 10, 5)
                    red_bullets.append(bullet)
                    red.shoot(bullet.x, bullet.y, RED_LASER_ROTATED)

                if event.key == pygame.K_CAPSLOCK and yellow.orientation == 'east':
                    bullet = pygame.Rect(yellow.x, yellow.y - 20, 10, 5)
                    yellow_bullets.append(bullet)
                    yellow.shoot(bullet.x, bullet.y, YELLOW_LASER_ROTATED)

                if event.key == pygame.K_CAPSLOCK and yellow.orientation == 'west':
                    bullet = pygame.Rect(yellow.x - yellow.get_width() / 2 - 10, yellow.y - 20, 10, 5)
                    yellow_bullets.append(bullet)
                    yellow.shoot(bullet.x, bullet.y, YELLOW_LASER_ROTATED)

        keys = pygame.key.get_pressed()

        handle_player_movements(keys, yellow, red)

        yellow.cool_down()
        red.cool_down()

        yellow.move_lasers(BULLET_VEL)
        red.move_lasers(BULLET_VEL)

        # create meteors with numbered answers blitted on them

        if len(upper_meteors) == 0 and len(lower_meteors) == 0:
            question, answer = random.choice(list(math_problems.items()))
            potential_answers = list(range(answer - 10, answer + 10))
            answers = random.sample(potential_answers, 5)
            if answer not in answers:
                answers.append(answer)

            for number in answers:
                choice = random.choice(range(1, 5))
                is_answer = False

                if choice == 1:
                    if number == answer:
                        is_answer = True
                    meteor = MeteorOne(random.choice(range(WIDTH - 350, WIDTH)),
                                       random.choice(range(-450, 100)), METEOR_ONE_SCALED, number, is_answer)
                    upper_meteors.append(meteor)

                elif choice == 2:
                    if number == answer:
                        is_answer = True

                    meteor = MeteorTwo(random.choice(range(0, 350)),
                                       random.choice(range(-450, 100)), METEOR_TWO_SCALED, number, is_answer)
                    upper_meteors.append(meteor)

                elif choice == 3:
                    if number == answer:
                        is_answer = True

                    meteor = MeteorThree(random.choice(range(0, 350)),
                                         random.choice(range(HEIGHT, HEIGHT + 150)),
                                         METEOR_THREE_SCALED, number, is_answer)

                    lower_meteors.append(meteor)

                elif choice == 4:
                    if number == answer:
                        is_answer = True

                    meteor = MeteorFour(random.choice(range(WIDTH - 350, WIDTH)),
                                        random.choice(range(HEIGHT, HEIGHT + 100)),
                                        METEOR_FOUR_SCALED, number, is_answer)

                    lower_meteors.append(meteor)

        # handle meteor entering from upper screen

        for meteor in upper_meteors[:]:
            meteor.move_meteor(METEOR_VEL)

            if collide(yellow, meteor):
                yellow.health -= 5
                upper_meteors.remove(meteor)
                gun_hit = pygame.mixer.Sound('button-22.wav')
                gun_hit.play()

            if collide(red, meteor):
                red.health -= 5
                upper_meteors.remove(meteor)
                gun_hit = pygame.mixer.Sound('button-22.wav')
                gun_hit.play()

            for laser in red.lasers:

                # check if laser is off screen and remove if so

                if not laser.check_if_laser_on_screen():
                    red.lasers.remove(laser)

                # check if yellow hit

                if collide(laser, yellow):
                    yellow.health -= 5
                    red.lasers.remove(laser)

                    gun_hit = pygame.mixer.Sound('Assets_Grenade+1.mp3')
                    gun_hit.play()

                # check collision with upper_meteors

                if collide(laser, meteor) and meteor.answer is True:
                    red.health += 10
                    upper_meteors.clear()
                    lower_meteors.clear()
                    red.lasers.remove(laser)

                    gun_hit = pygame.mixer.Sound('Assets_Grenade+1.mp3')
                    gun_hit.play()

                elif collide(laser, meteor) and meteor.answer is not True:
                    red.health -= 5
                    upper_meteors.remove(meteor)
                    red.lasers.remove(laser)

                    gun_hit = pygame.mixer.Sound('beep-25.wav')
                    gun_hit.play()

            for laser in yellow.lasers:

                # check if yellow laser is off screen and remove if so

                if not laser.check_if_laser_on_screen():
                    yellow.lasers.remove(laser)

                # check if red hit

                if collide(laser, red):
                    red.health -= 5
                    yellow.lasers.remove(laser)

                    gun_hit = pygame.mixer.Sound('Assets_Grenade+1.mp3')
                    gun_hit.play()

                # check collision with upper_meteors

                if collide(laser, meteor) and meteor.answer is True:
                    yellow.health += 10
                    upper_meteors.clear()
                    lower_meteors.clear()
                    yellow.lasers.remove(laser)

                    gun_hit = pygame.mixer.Sound('Assets_Grenade+1.mp3')
                    gun_hit.play()

                elif collide(laser, meteor) and meteor.answer is not True:
                    yellow.health -= 5
                    upper_meteors.remove(meteor)
                    yellow.lasers.remove(laser)

                    gun_hit = pygame.mixer.Sound('beep-25.wav')
                    gun_hit.play()

            if not meteor.check_if_on_screen():
                upper_meteors.remove(meteor)

        for meteor in lower_meteors[:]:
            meteor.move_meteor(METEOR_VEL)

            if collide(yellow, meteor):
                yellow.health -= 5
                lower_meteors.remove(meteor)
                gun_hit = pygame.mixer.Sound('button-22.wav')
                gun_hit.play()

            if collide(red, meteor):
                red.health -= 5
                lower_meteors.remove(meteor)
                gun_hit = pygame.mixer.Sound('button-22.wav')
                gun_hit.play()

            for laser in red.lasers:

                # check collision with upper_meteors

                if collide(laser, meteor) and meteor.answer is True:
                    red.health += 10
                    lower_meteors.clear()
                    upper_meteors.clear()
                    red.lasers.remove(laser)

                    gun_hit = pygame.mixer.Sound('Assets_Grenade+1.mp3')
                    gun_hit.play()

                elif collide(laser, meteor) and meteor.answer is not True:
                    red.health -= 5
                    lower_meteors.remove(meteor)
                    red.lasers.remove(laser)

                    gun_hit = pygame.mixer.Sound('beep-25.wav')
                    gun_hit.play()

            for laser in yellow.lasers:

                # check collision with upper_meteors

                if collide(laser, meteor) and meteor.answer is True:
                    yellow.health += 10
                    lower_meteors.clear()
                    upper_meteors.clear()
                    yellow.lasers.remove(laser)

                    gun_hit = pygame.mixer.Sound('Assets_Grenade+1.mp3')
                    gun_hit.play()

                elif collide(laser, meteor) and meteor.answer is not True:
                    yellow.health -= 5
                    lower_meteors.remove(meteor)
                    yellow.lasers.remove(laser)

                    gun_hit = pygame.mixer.Sound('beep-25.wav')
                    gun_hit.play()

            if not meteor.check_if_on_screen():
                lower_meteors.remove(meteor)

        # create lists of asteroid (upper & lower) - maximum 2

        if len(upper_asteroids) + len(lower_asteroids) < 2:

            # use random to decide whether asteroid appears on top or on bottom

            selection = random.choice(range(1, 3))

            if selection == 1:
                # use random to decide whether the answer is true or false

                second_selection = random.choice(range(1, 3))

                if second_selection == 1:
                    # use random to choose a random TRUE statement to blit on asteroid
                    statement = random.choice(true_statements)
                    asteroid = Asteroid(random.choice(range(0, WIDTH - ASTEROID_WIDTH)),
                                        random.choice(range(-150 - ASTEROID_HEIGHT, 50 - ASTEROID_HEIGHT)),
                                        ASTEROID_SCALED, ASTEROID_VEL, statement, True)
                    upper_asteroids.append(asteroid)

                elif second_selection == 2:
                    # use random to choose a random FALSE statement to blit on asteroid
                    statement = random.choice(false_statements)
                    asteroid = Asteroid(random.choice(range(0, WIDTH - ASTEROID_WIDTH)),
                                        random.choice(range(-150 - ASTEROID_HEIGHT, 50 - ASTEROID_HEIGHT)),
                                        ASTEROID_SCALED, ASTEROID_VEL, statement, False)
                    upper_asteroids.append(asteroid)

            elif selection == 2:
                # use random to decide whether the answer is true or false

                second_selection = random.choice(range(1, 3))

                if second_selection == 1:
                    # use random to choose a random TRUE statement to blit on asteroid
                    statement = random.choice(true_statements)
                    asteroid = Asteroid(int(random.choice(range(50, WIDTH - ASTEROID_WIDTH))),
                                        int(random.choice(range(HEIGHT + 50, HEIGHT + 200))), ASTEROID_SCALED,
                                        -ASTEROID_VEL, statement, True)
                    lower_asteroids.append(asteroid)

                elif second_selection == 2:
                    # use random to choose a random FALSE statement to blit on asteroid
                    statement = random.choice(false_statements)
                    asteroid = Asteroid(int(random.choice(range(0, WIDTH - ASTEROID_WIDTH))),
                                        int(random.choice(range(HEIGHT + 50, HEIGHT + 200))), ASTEROID_SCALED,
                                        -ASTEROID_VEL, statement, False)
                    lower_asteroids.append(asteroid)

        # Handle asteroids that come up from the top

        for asteroid in upper_asteroids[:]:
            asteroid.move_asteroid()
            if not asteroid.lower_check_if_on_screen():
                upper_asteroids.remove(asteroid)

            # check for asteroid/ player collision

            if collide(asteroid, yellow):
                yellow.health -= 5
                upper_asteroids.remove(asteroid)
                gun_hit = pygame.mixer.Sound('button-22.wav')
                gun_hit.play()

            if collide(red, asteroid):
                red.health -= 5
                upper_asteroids.remove(asteroid)
                gun_hit = pygame.mixer.Sound('button-22.wav')
                gun_hit.play()

            # check for laser and asteroid collision

            for laser in red.lasers:
                if collide(laser, asteroid):
                    red.lasers.remove(laser)
                    asteroid.lives -= 1

                    if asteroid.lives > 0:
                        gun_hit = pygame.mixer.Sound('Assets_Grenade+1.mp3')
                        gun_hit.play()

                    else:
                        # check whether the answer was correct
                        if asteroid.correct:
                            red.health += 5
                            upper_asteroids.remove(asteroid)
                            gun_hit = pygame.mixer.Sound('Explosion+3.wav')
                            gun_hit.play()

                        else:
                            red.health -= 5
                            upper_asteroids.remove(asteroid)
                            gun_hit = pygame.mixer.Sound('beep-25.wav')
                            gun_hit.play()

            for laser in yellow.lasers:
                if collide(laser, asteroid):
                    yellow.lasers.remove(laser)
                    asteroid.lives -= 1

                    if asteroid.lives > 0:
                        gun_hit = pygame.mixer.Sound('Assets_Grenade+1.mp3')
                        gun_hit.play()

                    else:
                        # check whether the answer was correct
                        if asteroid.correct:
                            yellow.health += 5
                            upper_asteroids.remove(asteroid)
                            gun_hit = pygame.mixer.Sound('Explosion+5.wav')
                            gun_hit.play()

                        else:
                            yellow.health -= 5
                            upper_asteroids.remove(asteroid)
                            gun_hit = pygame.mixer.Sound('beep-25.wav')
                            gun_hit.play()

        # Handle asteroids that come up from the bottom

        for asteroid in lower_asteroids[:]:
            asteroid.move_asteroid()

            if not asteroid.upper_check_if_on_screen():
                lower_asteroids.remove(asteroid)

            # check for player collision

            if collide(yellow, asteroid):
                yellow.health -= 5
                lower_asteroids.remove(asteroid)
                gun_hit = pygame.mixer.Sound('button-22.wav')
                gun_hit.play()

            if collide(red, asteroid):
                red.health -= 5
                lower_asteroids.remove(asteroid)
                gun_hit = pygame.mixer.Sound('button-22.wav')
                gun_hit.play()

            # check for laser and asteroid collision

            for laser in red.lasers:
                if collide(laser, asteroid):
                    red.lasers.remove(laser)
                    asteroid.lives -= 1

                    if asteroid.lives > 0:
                        gun_hit = pygame.mixer.Sound('Assets_Grenade+1.mp3')
                        gun_hit.play()

                    else:
                        # check whether the answer was correct
                        if asteroid.correct:
                            red.health += 5
                            lower_asteroids.remove(asteroid)
                            gun_hit = pygame.mixer.Sound('Explosion+8.wav')
                            gun_hit.play()

                        else:
                            red.health -= 5
                            lower_asteroids.remove(asteroid)
                            gun_hit = pygame.mixer.Sound('beep-25.wav')
                            gun_hit.play()

            for laser in yellow.lasers:
                if collide(laser, asteroid):
                    yellow.lasers.remove(laser)
                    asteroid.lives -= 1

                    if asteroid.lives > 0:
                        gun_hit = pygame.mixer.Sound('Assets_Grenade+1.mp3')
                        gun_hit.play()

                    if asteroid.lives <= 0:
                        # check whether the answer was correct
                        if asteroid.correct:
                            yellow.health += 5
                            lower_asteroids.remove(asteroid)
                            gun_hit = pygame.mixer.Sound('Explosion+10.wav')
                            gun_hit.play()

                        else:
                            yellow.health -= 5
                            lower_asteroids.remove(asteroid)
                            gun_hit = pygame.mixer.Sound('beep-25.wav')
                            gun_hit.play()

        # check if someone has lost or if time is up

        winner = check_if_loser(yellow, red)

        if winner is not None:
            lost = True
            lost_count += 1

        if seconds_remaining <= 0:
            lost = True
            lost_count += 1

            if red.health > yellow.health:
                winner = "Red Wins!"
            elif yellow.health > red.health:
                winner = "Yellow Wins!"
            elif yellow.health == red.health:
                winner = "Draw game!"


def main_menu():
    run = True

    clock = pygame.time.Clock()

    while run:
        fps_count = 0
        countdown_seconds = 5

        clock.tick(FPS)

        WIN.blit(SPACE_FOR_MENU, (0, 0))
        intro_text = INTRO_FONT.render("Click Mouse Button to Begin", True, WHITE)
        WIN.blit(intro_text, (WIDTH / 2 - intro_text.get_width() / 2, HEIGHT / 2 - intro_text.get_height() / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                while countdown_seconds > 0:
                    WIN.blit(SPACE_FOR_MENU, (0, 0))
                    seconds = INTRO_FONT.render(str(countdown_seconds), True, WHITE)
                    WIN.blit(seconds, (WIDTH / 2 - seconds.get_width() / 2, HEIGHT / 2 - seconds.get_height() / 2))
                    fps_count += 1
                    pygame.display.update()

                    if fps_count >= 700:
                        countdown_seconds -= 1
                        fps_count = 0

                main()

    pygame.quit()


if __name__ == "__main__":
    main_menu()
