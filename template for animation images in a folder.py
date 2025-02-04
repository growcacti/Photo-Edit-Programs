import os
import pygame as pg









image_folder = "path/to/folder"  # Replace with the path to your image folder
image_list = []
image_folder = "path/to/folder"  # Replace with the path to your image folder
for filename in os.listdir(image_folder):
    image_path = os.path.join(image_folder, filename)
    if os.path.isfile(image_path):
        image = pg.image.load(image_path).convert_alpha()
        image_list.append(image)
image_list.sort()
screen = pg.display.set_mode((800, 600))  # Replace with your desired screen size

# Set up animation parameters
animation_fps = 10  # Frames per second
animation_delay = 1000 // animation_fps  # Delay between frames in milliseconds
current_frame = 0
animation_done = False

# Main game loop
clock = pg.time.Clock()
while not animation_done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            animation_done = True

    # Clear the screen
    screen.fill((0, 0, 0))

    # Get the current frame image from the image list
    current_image = image_list[current_frame]

    # Blit the current frame image onto the screen
    screen.blit(current_image, (0, 0))

    # Update the frame index
    current_frame = (current_frame + 1) % len(image_list)

    # Update the display
    pg.display.flip()

    # Delay to achieve the desired frame rate
    clock.tick(animation_fps)

# Quit the game
pg.quit()
