from os import system
from tkinter import CENTER
import pygame                                   #import pygame
from sys import exit
from random import randint #getting random intiger

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time #rounding down from ms to secounds and getting rid of float numbers by throwing to int
    score_surf = test_font.render(f"Score: {current_time}", False, (64,64,64)) #creating a surface for text (what f"{}" does is converting int to string, because text function needs string as imput)
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 400:
                screen.blit(orc_surf, obstacle_rect)
            else: 
                screen.blit(bird_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] #deleting already generated obstacles if they're off screen

        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True                

def player_animation():
    global player_surf, player_index    
    if player_rect.bottom < 400:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk) : player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()                                   #initialize pygame
screen = pygame.display.set_mode((800,400)) 
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf",50)   #used to set a font that we can display first is type and then size, with type None it's a default font of pygame
game_active = True
start_time = 0
score = 0

#test_surface = pygame.Surface((100,200))       just displays red rectangle
#test_surface.fill("Red")

background = pygame.image.load("graphics/background.png").convert() #convert alpha converts a file to a type that pygame can work with more easily, in theory this should make the game run faster
ground = pygame.image.load("graphics/ground.png").convert_alpha()

# score_surf = test_font.render("My game", False, (64,64,64))  #text we want to display/anti aliasing/color
# score_rect = score_surf.get_rect(center = (400,50))

#obstacles
orc_surf = pygame.image.load("graphics/orc.png").convert_alpha()
#orc_rect = orc_surf.get_rect(midbottom = (600,400)) (don't need it if we're using obstacle list)
orc_going_left = True

bird_surf = pygame.image.load("graphics/bird.png").convert_alpha()

obstacle_rect_list = []

#player
player_walk_1 = pygame.image.load("graphics/lizard_protag1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/lizard_protag2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/lizard_protag_jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (200,400)) #creates a rectangle inside which the surface is placed, which allows for more comfortable point grabbing when it comes to placement
player_gravity = 0

#intro screen
player_stand = pygame.image.load("graphics/lizard_protag.png").convert_alpha()
player_stand = pygame.transform.scale(player_stand,(72*2,93*2))
player_stand = pygame.transform.rotate(player_stand,90)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render("Pixel Runner", False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render("Press space to run", False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))

#Timer
obstacle_timer = pygame.USEREVENT + 1 #the reason for it is that there are already some events that are already reserved for pygame, to avoid conflict we have to add +1 to each event we are going to add
pygame.time.set_timer(obstacle_timer,1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            # if event.type == pygame.MOUSEMOTION: #this lets us to check the position or if button is pressed
            #     print(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse down")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(pygame.mouse.get_pos()) and player_rect.bottom == 400: # event.pos works as well
                    player_gravity = -15

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 400:
                    player_gravity = -15

            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(orc_surf.get_rect(midbottom = (randint(900,1100),400)))
                else:
                    obstacle_rect_list.append(bird_surf.get_rect(midbottom = (randint(900,1100),210)))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                #orc_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)
        
        

    if game_active:  
        screen.blit(background,(0,0))  
        screen.blit(ground,(0,320))
        # pygame.draw.rect(screen,"#c0e8ec",score_rect)
        # pygame.draw.rect(screen,"#c0e8ec",score_rect,10)
        # screen.blit(score_surf,score_rect) 
        #pygame.draw.line(screen,"Red",(0,0),(800,400),5) #draws a line
        #pygame.draw.ellipse(screen,"Brown",pygame.Rect(50,200,100,100)) #draws an ellipse
        score = display_score()

        #orc (don't need it if we're using obstacle list)
        if False:
            orc_speed = 5
            if orc_going_left == True and orc_rect.x > 0:
                orc_rect.x -= orc_speed
            else:
                orc_going_left = False
            if orc_going_left == False and orc_rect.x < 720:
                orc_rect.x += orc_speed
            else:
                orc_going_left = True

            screen.blit(orc_surf,orc_rect)

        #player
        player_gravity += 0.5
        player_rect.y += player_gravity
        if player_rect.bottom > 400: player_rect.bottom = 400
        player_animation()
        screen.blit(player_surf,player_rect)

        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision
        # if orc_rect.colliderect(player_rect):
        game_active = collisions(player_rect,obstacle_rect_list)
        
        if False:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                print("jump")

            if player_rect.colliderect(orc_rect): print("collision")      #checking if player collides with enemy
            else: print("nocollision")
            
            mouse_pos = pygame.mouse.get_pos()
            if player_rect.collidepoint(mouse_pos):   #checking if cursor collides with player and then checking if there are any buttons pressed
                print(pygame.mouse.get_pressed())
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (200,400)

        score_message = test_font.render(f"Your score: {score}", False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)

        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    pygame.display.update()                     #updates display surface
    clock.tick(60)                              #this tells the loop that it shouldn't run faster than 60fps
    #draw all out elements
    #update everything

