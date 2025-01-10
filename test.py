import pygame
import random

# Initialize Pygame
pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

# This is setting the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Striker's Paradise")

# Load and scale background image
background_image = pygame.image.load('Images/Field.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load logo image
logo_image = pygame.image.load('Images/logo.png')
logo_image = pygame.transform.scale(logo_image, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

class GoalMouth(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
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

        one_player_text = small_font.render("Press 1 for 1 Player", True, BLACK)
        screen.blit(one_player_text, (SCREEN_WIDTH // 2 - one_player_text.get_width() // 2, 400))

        two_player_text = small_font.render("Press 2 for 2 Players", True, BLACK)
        screen.blit(two_player_text, (SCREEN_WIDTH // 2 - two_player_text.get_width() // 2, 450))

        pygame.display.flip()

def main_game(mode):
    players_team1 = [Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + i * 30, BLACK) for i in range(11)]
    players_team2 = [Player(3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + i * 30, WHITE) for i in range(11)]
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    goalmouth1 = GoalMouth(50, SCREEN_HEIGHT // 2, 10, 100)
    goalmouth2 = GoalMouth(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2, 10, 100)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(*players_team1, *players_team2, ball, goalmouth1, goalmouth2)
 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    mode = main_menu()
    main_game(mode)