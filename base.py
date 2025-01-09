import pygame

# Initialize Pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# This is setting the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Striker's Paradise")

# Load background image
background_image = pygame.image.load('path_to_your_image.jpg')

class player:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game elements here

    # Render game elements here
    screen.blit(background_image, (0, 0))
    pygame.display.flip()

pygame.quit()










#Reference
# https://www.pygame.org/docs/