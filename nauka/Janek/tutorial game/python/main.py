from os import system
from tkinter import CENTER
import pygame                                   #import pygame
from sys import exit
from random import randint, choice #getting random intiger

class Player(pygame.sprite.Sprite): #this has to inherit from another class
    def __init__(self):  #he __init__ method is the Python equivalent of the C++ constructor in an object-oriented approach. The __init__  function is called every time an object is created from a class. The __init__ method lets the class initialize the object’s attributes and serves no other purpose. It is only used within classes. 
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/lizard_protag1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/lizard_protag2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/lizard_protag_jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,400))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 400 and score != 0:
            self.gravity = -15
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.y += self.gravity
        if self.rect.bottom >= 400:
            self.rect.bottom = 400
    
    def animation_state(self):
        if self.rect.bottom < 400:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)] 
    
    def place_player_onGround(self):
        self.gravity = 0
        self.rect.bottom = 400

    def update(self):
        if game_active:
            self.player_input()
            self.apply_gravity()
            self.animation_state()
        else:
            self.place_player_onGround()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type): #type decides whether it's a bird or an orc
        super().__init__()

        if type == "bird":
            bird_1 = pygame.image.load("graphics/bird/bird0000.png").convert_alpha()
            bird_2 = pygame.image.load("graphics/bird/bird0001.png").convert_alpha()
            bird_3 = pygame.image.load("graphics/bird/bird0002.png").convert_alpha()
            self.frames = [bird_1,bird_2,bird_3]
            y_pos = 210
        else:
            orc_1 = pygame.image.load("graphics/orc/orc0000.png").convert_alpha()
            orc_2 = pygame.image.load("graphics/orc/orc0001.png").convert_alpha()
            self.frames = [orc_1,orc_2]
            y_pos = 400

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time #rounding down from ms to secounds and getting rid of float numbers by throwing to int
    score_surf = test_font.render(f"Score: {current_time}", False, (64,64,64)) #creating a surface for text (what f"{}" does is converting int to string, because text function needs string as imput)
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time               

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False): #player is a GroupSingle that contains a sprite since this class has only one sprite it's workable, in a regular group this sprite would not work since we'd get a list, so that's why we're using GroupSingle. NEXT is obstacle_group this checks if our player sprite collides with sprite from obstacle_group, the boolean decides whether after collision the obstacle sprite is deleted or not
        obstacle_group.empty() #empties obstacle group after collison so the sprite doesn't stay in same spot causing the game to crash every time we want to continue
        return False
    else: return True

pygame.init()                                   #initialize pygame
screen = pygame.display.set_mode((800,400)) 
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf",50)   #used to set a font that we can display first is type and then size, with type None it's a default font of pygame
game_active = True
start_time = 0
score = 0
bgm = pygame.mixer.Sound("audio/Drakecelsior.mp3")
bgm.set_volume(0.5)
bgm.play(loops = -1) #plays the music and tells it to play forever

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#test_surface = pygame.Surface((100,200))       just displays red rectangle
#test_surface.fill("Red")

background = pygame.image.load("graphics/background.png").convert() #convert alpha converts a file to a type that pygame can work with more easily, in theory this should make the game run faster
ground = pygame.image.load("graphics/ground.png").convert_alpha()

# score_surf = test_font.render("My game", False, (64,64,64))  #text we want to display/anti aliasing/color
# score_rect = score_surf.get_rect(center = (400,50))

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse down")

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["bird","orc","orc","orc"]))) #choice picks one of these 4 items, since there's 3 orcs and 1 bird there's 75% chance for an orc and 25% for a bird
                        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        
        

    if game_active:  
        #display background and score
        screen.blit(background,(0,0))  
        screen.blit(ground,(0,320))
        score = display_score()

        #player
        player.draw(screen)
        player.update()

        #obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        #collision
        game_active = collision_sprite()
        
    else:
        #game over screen
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        player.update()
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

