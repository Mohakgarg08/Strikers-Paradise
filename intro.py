import pygame

# Initialize Pygame
pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

# This is setting the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Striker's Paradise")

# Load and scale background image
background_image = pygame.image.load('Field.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load logo image
logo_image = pygame.image.load('logo.png')
logo_image = pygame.transform.scale(logo_image, (SCREEN_WIDTH//4, SCREEN_HEIGHT//4))
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

#def player():
# Define player properties








# Intro screen
def intro_screen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2

        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))
        screen.blit(logo_image, (SCREEN_WIDTH // 2 - logo_image.get_width() // 2, 100))

        title_text = font.render("Striker's Paradise", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 300))

        one_player_text = small_font.render("Press 1 for 1 V COMPUTER", True, BLACK)
        screen.blit(one_player_text, (SCREEN_WIDTH // 2 - one_player_text.get_width() // 2, 400))

        two_player_text = small_font.render("Press 2 for Multiplayer", True, BLACK)
        screen.blit(two_player_text, (SCREEN_WIDTH // 2 - two_player_text.get_width() // 2, 450))

        pygame.display.flip()

# Main game loop
def main_game(mode):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Render game elements here
        screen.blit(background_image, (0, 0))
        pygame.display.flip()

    pygame.quit()

# Run the intro screen
game_mode = intro_screen()
main_game(game_mode)