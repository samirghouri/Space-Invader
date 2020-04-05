import pygame
import random
import math

# to initialise all the pygame module
pygame.init()

# create the screen of 800x600 pixcels
screen = pygame.display.set_mode((800,600))

# loading the background image
background = pygame.image.load("background.jpg")

# changing the caption and icon
pygame.display.set_caption("Spaec Invader")
icon = pygame.image.load("rocket.png")
pygame.display.set_icon(icon)

# player 
player_img = pygame.image.load("player.png")
player_x = 400
player_y = 500
playerX_change = 0

# enemy
enemy_img = list()
enemy_x = list()
enemy_y = list()
enemyX_change = list()
enemyY_change = list()
max_enemies = 6

for i in range(max_enemies):
    enemy_img.append( pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0,704))
    enemy_y.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# bullet
# ready -> you can see it on the scree
# fire -> bullet is currently moving 
bullet_img = pygame.image.load("fire.png")
bullet_x =0
bullet_y = 500 # because our player is stating at this postion 
bulletX_change = 0
bulletY_change = 8
bullet_state = "ready"

# adding the score 
score_value = 0
font = pygame.font.Font("Pintersan.ttf" , 32)
text_x = 10
text_y = 10

# game over
font_game_over = pygame.font.Font("Pintersan.ttf" ,64)
game_over_x = 300
game_over_y = 300

def game_over():
    gam_over = font_game_over.render("Game Over",True, (255,255,255))
    screen.blit(gam_over,(game_over_x,game_over_y))

def show_score():
    score = font.render("Score :" +str(score_value), True , (255,255,255))
    screen.blit(score ,(text_x,text_y))


def player(x,y):
    screen.blit(player_img,(x,y))

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img,(x+16,y+10))


def is_collision(bullet_x,bullet_y,enemy_x,enemy_y):
    distance = math.sqrt((math.pow(enemy_x-bullet_x,2))+math.pow(enemy_y-bullet_y,2))
    if distance < 35:
        return True
    else:
        return False

#making a game loop untile the game is closed
running = True
while running:
    # RGB -red , green , blue
    screen.fill((0,0,0))

    # background image addtion
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
        # the KEYDOWN means a key is pressed 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            elif event.key == pygame.K_RIGHT:
                playerX_change = 2
        # the KEYUP means that the key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x,bullet_y)
        
    player_x += playerX_change


    # setting a boundary for the player so that it doest go out of screen
    if player_x<0:
        player_x = 0
    elif player_x >752:
        player_x = 752
        
    for i in range(max_enemies):
        if enemy_y[i]> 420:
            for j in range(max_enemies):
                enemy_y[j]=2000
            game_over()
            break

        enemy_x[i] += enemyX_change[i]

        # setting a boundary for thr enemy so that it doest go out of screen
        if enemy_x[i] <= 0:
            enemyX_change[i] = 2
            enemy_y[i] += enemyY_change[i]
    
        elif enemy_x[i] >= 704:
            enemyX_change[i] = -2
            enemy_y[i] += enemyY_change[i]
         # collision
   
        collision = is_collision(bullet_x,bullet_y,enemy_x[i],enemy_y[i])
        if collision:
            bullet_y = 500
            score_value +=1
            bullet_state = "ready"
            enemy_x[i] = random.randint(0,704)
            enemy_y[i] = random.randint(50,150)
            print(score_value)
        enemy(enemy_x[i],enemy_y[i],i)

    
    # moving the bullet
    if bullet_y <= 0:
        bullet_state = "ready"
        bullet_y = 500
    if bullet_state == "fire":
        fire_bullet(bullet_x,bullet_y)
        bullet_y -= bulletY_change

   
        
 
    player(player_x,player_y)
    show_score()
    pygame.display.update()
