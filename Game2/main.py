import pygame
from pygame.locals import *

pygame.init()

screen_w = 1024
screen_h = 1024
tile_s = 64

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Drakeceisior')



bg_img = pygame.image.load("bg.jpg")

def draw_g():
	for line in range(0, 16):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_s), (screen_w, line * tile_s))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_s, 0), (line * tile_s, screen_h))


class Player():
    def __init__(self, x, y):
        img = pygame.image.load('cat.png')
        self.image = pygame.transform.scale(img, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        dx = 0
        dy = 0

        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            dy -= 4
        if key[pygame.K_a]:
            dx -= 4
        if key[pygame.K_s]:
            dy += 4
        if key[pygame.K_d]:
            dx += 4


         #check for collision
        for tile in world.tile_list:
            #check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
               	dy = 0




        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        #draw player onto screen
        screen.blit(self.image, self.rect)


class World():
	def __init__(self, data):
		self.tile_list = []

		dirt_img = pygame.image.load('wall.png')
		hero_img = pygame.image.load("icon.png")

		row_c = 0
		for row in data:
			col = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_s, tile_s))
					img_rect = img.get_rect()
					img_rect.x = col * tile_s
					img_rect.y = row_c * tile_s
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(hero_img, (tile_s, tile_s))
					img_rect = img.get_rect()
					img_rect.x = col * tile_s
					img_rect.y = row_c * tile_s
					tile = (img, img_rect)
					self.tile_list.append(tile)
				col += 1
			row_c += 1
	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
[1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

world = World(world_data)
player = Player(640, 704)

run = True
while run:

	screen.blit(bg_img, (0, 0))

	world.draw()

	player.update()

	draw_g()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()
pygame.quit()