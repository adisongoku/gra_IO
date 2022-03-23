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

#bird
bird_1 = pygame.image.load("graphics/bird/bird0000.png").convert_alpha()
bird_2 = pygame.image.load("graphics/bird/bird0001.png").convert_alpha()
bird_3 = pygame.image.load("graphics/bird/bird0002.png").convert_alpha()
bird_frames = [bird_1,bird_2,bird_3]
bird_frame_index = 0
bird_surf = bird_frames[bird_frame_index]

#orc
orc_1 = pygame.image.load("graphics/orc/orc0000.png").convert_alpha()
orc_2 = pygame.image.load("graphics/orc/orc0001.png").convert_alpha()
orc_frames = [orc_1,orc_2]
orc_frame_index = 0
orc_surf = orc_frames[orc_frame_index]

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
pygame.time.set_timer(obstacle_timer, 1500)

orc_animation_timer = pygame.USEREVENT+2
pygame.time.set_timer(orc_animation_timer, 500)

bird_animation_timer = pygame.USEREVENT+3
pygame.time.set_timer(bird_animation_timer, 200)

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

            if event.type == orc_animation_timer:
                if orc_frame_index == 0: orc_frame_index = 1
                else: orc_frame_index = 0
                orc_surf = orc_frames[orc_frame_index]

            if event.type == bird_animation_timer:
                if bird_frame_index == 0: bird_frame_index = 1
                else: bird_frame_index = 0
                bird_surf = bird_frames[bird_frame_index]
            
            
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                #orc_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)
        
        

    if game_active:  
        screen.blit(background,(0,0))  
        screen.blit(ground,(0,320))
        score = display_score()

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

