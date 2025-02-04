# Pygame template - skeleton for a new pygame project
import pygame
import random
import os

WIDTH = 800
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up assets folders
game_folder = os.path.dirname(__file__)


#initialize pygame create window, and clock
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Template")
clock = pygame.time.Clock()

# Making a sprite group
all_sprites = pygame.sprite.Group()

path = "gx/bg"
filenames = [f for f in os.listdir(path) if f.endswith('.png')]
imagelist = []
for name in filenames:
    imagename = os.path.splitext(name)[0] 
    imagelist.append(pg.image.load(os.path.join(path, name)).convert_alpha())
   


def drop_enemies(enemy_list):
delay = random.random()
if len(enemy_list) < 10 and delay < 0.1:
    x_pos = random.randint(0, WIDTH - enemy_size)
    y_pos = 0
    enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
for enemy_pos in enemy_list:
    pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))




# Game loop
running = True
while running:
    #if the loop takes less than 1/30th of a second, this keeps the rate steady
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # Checking for quit
        if event.type == pygame.QUIT:
            running = False

    #Update
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # always flip last.  This is for double buffering.
    pygame.display.flip()






pygame.quit()
