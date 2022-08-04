from ast import Break
from operator import truediv
from pickle import FALSE, TRUE
import random
import math
import pygame
from pygame import mixer 

# Initialize the pygame
pygame.init()

# Create the Screen
screen = pygame.display.set_mode((800,600))

# Title And Icon
pygame.display.set_caption("Space Fighter")
icon=pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Background

background = pygame.image.load("background.png")

# Background music

bg_music = mixer.Sound('background.wav')
bg_music.play(-1)

# Player
playerImg= pygame.image.load("player.png")
playerX= 370
playerY= 520
playerX_change= 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies) :
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,768))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet

# ready = you can't see the bullet on the screen
# fire = the  bullet is moving on the screen 

bulletImg= pygame.image.load("bullet.png")
bulletX= 0
bulletY= 520
bulletX_change= 0
bulletY_change= 1
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('font.otf' ,42)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('font.otf' ,75)

# Credits
credits_font = pygame.font.Font('font.otf' ,39)


def show_score(x,y):
    score = font.render("Score : " + str(score_value),True, (224,224,224))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True, (224,224,224))
    screen.blit(over_text, (200,250))

def credits_text():
    credits_text = credits_font.render("CREDITS : Harkirat Singh",True, (224,224,224))
    screen.blit(credits_text, (172,350))
 
def player(x,y):
    screen.blit(playerImg, (x, y))
     
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+12))

# Applying distance formula:
# Sq.root of (X2-X1)^2 + (Y2-Y1)^2

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else :
        return False

#Game Loop
running = True
while running:

    #Background
    screen.fill((0,0,0))                             #black color
    screen.blit(background,(0,0))                    #Image

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False
        
        #If keystroke is pressed check whether it is right or left

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":

                    # Bullet Sound
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    #position                    
                    bulletX = playerX               
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
               playerX_change = 0            

    

   #Restricting player in a particular Boundary
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement

    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 490:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            credits_text()
            bg_music.stop()

            game_over_music = mixer.Sound('game_over.wav')
            game_over_music.play(-1)
            break

        enemyX[i] += enemyX_change[i] 
        if enemyX[i]  <= 0:
            enemyX_change[i]  = 0.4
            enemyY[i]  += enemyY_change[i] 
        elif enemyX[i]  >= 768:
            enemyX_change[i]  = -0.4
            enemyY[i]  += enemyY_change[i] 

        # Collision 
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision :
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 520
            bullet_state = "ready"
            score_value += 1            
            enemyX[i]= random.randint(0,768)
            enemyY[i]= random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement

    if bulletY <=0 :
        bulletY = 520
        bullet_state = "ready"

   
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

     


    

    player(playerX,playerY)
    show_score(textX,textY)    
    pygame.display.update()

   