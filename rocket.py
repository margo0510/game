import pygame 
import random
import time 
import os 

pygame.mixer.init()
pygame.font.init()

pygame.init()

WIDTH, HEIGHT = 900,500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space Invador")

WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
NAVY = (0,0,128)

BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound("assets/Grenade.mp3") #to load sounds
BULLET_FIRE_SOUND = pygame.mixer.Sound("assets/Gun_Silencer.mp3")

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("americantypewriter", 100)

BULLET_VEL = 7 
MAX_BULLETS = 3

FPS = 60 
VEL = 5

SPACESHIP_WIDTH, SPACESHIP_HEIGHT =  55,40

YELLOW_HIT = pygame.USEREVENT+1
RED_HIT = pygame.UNSEREVENT+2



player = pygame.image.load("character.png") #to load images 
bg_image = pygame.image.load("background.png")

yellow_spaceship_image = pygame.image.load(os.path.join("assets", "spaceship_yellow.png"))
yellow_spaceship = pygame.tranform.rotate(pygame.tranform.scale(yellow_spaceship_image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),90)

red_spaceship_image = pygame.image.load(os.path.join("assets", "spaceship_red.png"))
red_spaceship = pygame.tranform.rotate(pygame.tranform.scale(red_spaceship_image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),50)

space = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space.png")), (WIDTH,HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    screen.blit(space, (0,0))
    pygame.draw.rect(screen, NAVY, BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    screen.blit(red_health_text, (WIDTH - red_health_text.get_width()-10, 10))
    screen.blit(yellow_health_text, (10,10))

    screen.blit(red_spaceship, (red.x, red.y))
    screen.blit(yellow_spaceship, (yellow.x, yellow.y))

    for bullet in red_bullets:
        pygame.draw.rect(screen, RED, bullet )

    for bullet in yellow_bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    #using a,w,s,d to move yellow spaceship
    if keys_pressed[pygame.K_a] and yellow.x - VEL >0: 
        yellow.x -= VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL >0: 
        yellow.y -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.k_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    #using up, down, left and right arrow keys to move red spaceship 
    if keys_pressed[pygame.K_LEFT] and red.x - VEL >BORDER.x + BORDER.WIDTH:
        red.x -= VEL 
    if keys_pressed[pygame.K_UP] and red.y - VEL >0:
        red.y -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15 :
        red.y += VEL    

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet) 
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)   
