import pygame                                   #import pygame
from sys import exit

pygame.init()                                   #initialize pygame
screen = pygame.display.set_mode((800,400)) 
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf",50)   #used to set a font that we can display first is type and then size, with type None it's a default font of pygame

#test_surface = pygame.Surface((100,200))       just displays red rectangle
#test_surface.fill("Red")

background = pygame.image.load("graphics/background.png").convert() #convert alpha converts a file to a type that pygame can work with more easily, in theory this should make the game run faster
ground = pygame.image.load("graphics/ground.png").convert_alpha()
text_surface = test_font.render("My game", False, "Blue")  #text we want to display/anti aliasing/color

orc_surf = pygame.image.load("graphics/orc.png").convert_alpha()
orc_rect = orc_surf.get_rect(midbottom = (600,400))
orc_going_left = True

player_surf = pygame.image.load("graphics/lizard_protag.png")
player_rect = player_surf.get_rect(midbottom = (200,400)) #creates a rectangle inside which the surface is placed, which allows for more comfortable point grabbing when it comes to placement

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEMOTION: #this lets us to check the position or if button is pressed
            print(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("mouse down")
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos): print("collision") #checking if cursor collides with player

    screen.blit(background,(0,0))  
    screen.blit(ground,(0,320))
    screen.blit(text_surface,(300,50))  

    if orc_going_left == True and orc_rect.x > 0:
        orc_rect.x -= 1
    else:
        orc_going_left = False
    if orc_going_left == False and orc_rect.x < 720:
        orc_rect.x += 1
    else:
        orc_going_left = True

    screen.blit(orc_surf,orc_rect)
    screen.blit(player_surf,player_rect)

    # if player_rect.colliderect(orc_rect): print("collision")      #checking if player collides with enemy
    # else: print("nocollision")
    
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):   #checking if cursor collides with player and then checking if there are any buttons pressed
    #     print(pygame.mouse.get_pressed())

    pygame.display.update()                     #updates display surface
    clock.tick(60)                              #this tells the loop that it shouldn't run faster than 60fps
    #draw all out elements
    #update everything

