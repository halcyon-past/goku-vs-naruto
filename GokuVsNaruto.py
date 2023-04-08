import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()
pygame.init()

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("GOKU VS NARUTO!!!")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

BORDER = pygame.Rect(WIDTH/2-5,0,10,HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets','hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets','bullet.mp3'))
MUSIC = pygame.mixer.Sound(os.path.join('assets','BGM.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)
CRIT_FONT = pygame.font.SysFont('comicsans',70)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
ATTACK = [5,10,5,5,5,20,5,5,5,5,]
CHARACTER_WIDTH, CHARACTER_HEIGHT = 55,40

YELLOW_HIT = pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT +2


SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets','bg.jpg')),(WIDTH,HEIGHT))
GOKU_IMAGE = pygame.image.load(os.path.join('assets','goku.png'))
GOKU = pygame.transform.scale(GOKU_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
NARUTO_IMAGE = pygame.image.load(os.path.join('assets','naruto.png'))
NARUTO = pygame.transform.scale(NARUTO_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
YELLOW_BULLET = pygame.image.load(os.path.join('assets','fireball.png'))
YB = pygame.transform.rotate(pygame.transform.scale(YELLOW_BULLET, (10, 20)),180)
RED_BULLET = pygame.image.load(os.path.join('assets','rasengan.png'))
RB = pygame.transform.rotate(pygame.transform.scale(RED_BULLET, (10, 20)),270)

def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(SPACE ,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1 , WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1 , WHITE)
    WIN.blit(red_health_text, (WIDTH- red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text, (10,10))

    
    WIN.blit(GOKU, (yellow.x,yellow.y))
    WIN.blit(NARUTO, (red.x,red.y))
    

    for bullet in yellow_bullets:
        WIN.blit(YB,bullet)

    for bullet in red_bullets:
        WIN.blit(RB,bullet)

        
    pygame.display.update()
    
def yellow_handle_movement(keys_pressed,yellow):
    
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #right
        yellow.x += VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: #down
        yellow.y += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #up
        yellow.y -= VEL


def red_handle_movement(keys_pressed,red):
    
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + 5: #left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #right
        red.x += VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: #down
        red.y += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #up
        red.y -= VEL

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(winner_text):
    draw_text = WINNER_FONT.render(winner_text, 1, RED)
    WIN.blit(draw_text, (WIDTH//2-draw_text.get_width()//2,HEIGHT//2- draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def red_crit():
    crit_text = "GOKU CRIT"
    draw_text = CRIT_FONT.render(crit_text,1,YELLOW)
    WIN.blit(draw_text, (WIDTH//2-draw_text.get_width()//2,HEIGHT//4- draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(100)

def yellow_crit():
    crit_text = "NARUTO CRIT"
    draw_text = CRIT_FONT.render(crit_text,1,YELLOW)
    WIN.blit(draw_text, (WIDTH//2-draw_text.get_width()//2,HEIGHT//4- draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(100)

def major_crit_red():
    crit_text = "KAMEHAMEHA"
    draw_text = CRIT_FONT.render(crit_text,1,YELLOW)
    WIN.blit(draw_text, (WIDTH//2-draw_text.get_width()//2,HEIGHT//4- draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(100)

def major_crit_yellow():
    crit_text = "RASEN SHURIKEN"
    draw_text = CRIT_FONT.render(crit_text,1,YELLOW)
    WIN.blit(draw_text, (WIDTH//2-draw_text.get_width()//2,HEIGHT//4- draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(100)
    
    


def main():
    red = pygame.Rect(700,300,CHARACTER_WIDTH, CHARACTER_HEIGHT)
    yellow = pygame.Rect(100,300,CHARACTER_WIDTH, CHARACTER_HEIGHT)
    
    yellow_bullets = []
    red_bullets = []

    yellow_health = 100
    red_health = 100
    
    clock = pygame.time.Clock()
    run = True
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height//4 -2 , 10 ,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x,red.y + red.height//4 -2 , 10 ,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    

                    
            if event.type == RED_HIT:
                BULLET_HIT_SOUND.play()
                minus = random.choice(ATTACK)
                red_health -= minus
                if minus == 10:
                    red_crit()
                elif minus == 20:
                    major_crit_red()
                

            if event.type == YELLOW_HIT:
                BULLET_HIT_SOUND.play()
                minus = random.choice(ATTACK)
                yellow_health -= minus
                if minus == 10:
                    yellow_crit()
                elif minus == 20:
                    major_crit_yellow()

        winner_text = " "
        if red_health <= 0:
            winner_text = "Goku Wins!!"

        if yellow_health <= 0:
            winner_text = "Naruto Wins!!"

        if winner_text != " ":
            draw_winner(winner_text)
            break

        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)
        

    main()


if __name__ == "__main__":
    main()
