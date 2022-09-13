import pygame
import os
import time
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()
pygame.font.init()

# Create screen
Width, Height= 889,500
screen = pygame.display.set_mode((Width, Height))

background = pygame.image.load('spaceimg.png')
#background sound
mixer.music.load('Epic.mp3')
mixer.music.play(-1)

# Title change
pygame.display.set_caption("SPACE TRESPASSERS")

# Icon change, preferabble size 32px
icon = pygame.image.load('Spaceicon.png')
pygame.display.set_icon(icon)

# Player Icon
playerimg = pygame.image.load('player.png') 
playerX = 380
playerY = 400
playerX_change=0

# Enemy
enemyimg = []
enemyX =[]
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3

for i in range(num_of_enemies):

    enemyimg.append(pygame.image.load('Enemy1.png')) 
    enemyX.append( random.randint(0,825))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(20)

enemyimg2 = []
enemyX2 =[]
enemyY2 = []
enemyX_change2 = []
enemyY_change2 = []
num_of_enemies2 = 2

for j in range(num_of_enemies2):

    enemyimg2.append(pygame.image.load('Enemy3.png')) 
    enemyX2.append( random.randint(0,500))
    enemyY2.append(random.randint(50, 150))
    enemyX_change2.append(4)
    enemyY_change2.append(40)

# Bullet
bulletimg = pygame.image.load('bullet.png') 
bulletX = 0
#initial position as spaceship.
bulletY = 400 
bulletX_change = 0
bulletY_change = 10
bullet_state="ready"

#score
score = 0
font = pygame.font.Font('Sweet Chili Demo.ttf', 40)
#font = pygame.font.Font('Sweet Chili Demo.ttf', 40)
textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('Rolling Bold.ttf',70)

def game_over_text():
    over_text = over_font.render("GAME OVER",True, (255, 255, 255))
    screen.blit(over_text, (250,250))
   
def display_score(x,y):
    score_value = font.render("SCORE :" + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x,y))
pass
def player(x,y):
    screen.blit(playerimg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyimg[i], (x,y))

def enemy2(x,y,j):
    screen.blit(enemyimg2[j], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state ="fire"
    screen.blit(bulletimg,(x+16, y+10))

def iscollision(eX, eY, bX, bY):
    distance = math.sqrt(math.pow(eX-bX,2) + math.pow(eY-bY, 2))
    if distance < 27: #dist bw bullet n enemy, then collision.
        return True
    else:
        return False

# GAME LOOP

run = True
FPS = 60
clock = pygame.time.Clock()
while run:
    clock.tick(FPS)
    #background
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        #check whether quit button has pressed.
        if event.type == pygame.QUIT: 
            run = False
        # keystroke pressed or not and whether is left or not
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            elif event.key == pygame.K_SPACE: 
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        # If key is released or not.
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0 #space ship stops.
    #pass
    playerX += playerX_change

    if playerX <=0:
        playerX=0
    elif playerX >= 825:
        playerX = 825
# Enemy movement
    i=0
    j=0
    for i in range(num_of_enemies):
        #gameover
        if enemyY[i] > 300:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 825:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 400
            bullet_state = "ready"
            score += 1
            #print(score)
            enemyX[i] = random.randint(0,825)
            enemyY[i] = random.randint(50,150)
        enemy(enemyX[i], enemyY[i],i)

    for j in range(num_of_enemies2):
        #gameover
        if enemyY2[j] > 300:
            for k in range(num_of_enemies2):
                enemyY2[k] = 2000
            game_over_text()
            break
        enemyX2[j] += enemyX_change2[j]
        if enemyX2[j] <=0:
            enemyX_change2[j] = 2
            enemyY2[j] += enemyY_change2[j]
        elif enemyX2[j] >= 825:
            enemyX_change2[j] = -2
            enemyY2[j] += enemyY_change2[j]

        #collision
        collision2 = iscollision(enemyX2[j], enemyY2[j], bulletX, bulletY)
        if collision2:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score += 2
                #print(score)
                enemyX2[j] = random.randint(0,736)
                enemyY2[j] = random.randint(50,150)
        enemy2(enemyX2[j], enemyY2[j],j)

    #Bullet movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change  
    
    player(playerX, playerY)
    display_score(textX, textY)
    pygame.display.update()

