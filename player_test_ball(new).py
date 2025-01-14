import pygame, sys
import random

# Initialize Pygame
pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 30
PLAYER_SPEED = 7  # Increased player speed for smoother and faster movement
BALL_SPEED_X = 3  # Slower ball speed on the x-axis
BALL_SPEED_Y = 3  # Slower ball speed on the y-axis

#This is setting the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Striker's Paradise")

# Load and scale background image
background_image = pygame.image.load('Strikers-Paradise\Images\Field.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load logo image
logo_image = pygame.image.load('Strikers-Paradise\Images\Logo.png')
logo_image = pygame.transform.scale(logo_image, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Define fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = PLAYER_SPEED  # Adjusted speed for faster movement

    def update(self, keys, up, down, left, right):
        if keys[up] and self.rect.top > 0: 
            self.rect.y -= self.speed
        if keys[down] and self.rect.bottom < SCREEN_HEIGHT: 
            self.rect.y += self.speed
        if keys[left] and self.rect.left > 0: 
            self.rect.x -= self.speed
        if keys[right] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, imgpath, **kwargs):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Ball size
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.reset()

    def move(self, ball, racket_left, racket_right):
        self.rect.left = self.rect.left + self.speed * self.direction_x
        self.rect.top = min(max(self.rect.top + self.speed * self.direction_y, 0), SCREEN_HEIGHT - self.rect.height)

        # Collide with the left racket
        if pygame.sprite.collide_rect(ball, racket_left) or pygame.sprite.collide_rect(ball, racket_right):
            self.direction_x = -self.direction_x
            self.direction_y = random.choice([1, -1])
            self.speed += 1
        
        # Collide with top or bottom walls
        elif self.rect.top == 0:
            self.direction_y = 1
            self.speed += 1
        elif self.rect.bottom == SCREEN_HEIGHT:
            self.direction_y = -1
            self.speed += 1

        # Collide with the left wall (goal on right side)
        elif self.rect.left < 0:
            self.reset()
            racket_left.reset()
            racket_right.reset()
            return [0, 1]  # Left player scored
        
        # Collide with the right wall (goal on left side)
        elif self.rect.right > SCREEN_WIDTH:
            self.reset()
            racket_left.reset()
            racket_right.reset()
            return [1, 0]  # Right player scored

        return [0, 0]  # No score, normal movement

    def reset(self):
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = random.randrange(self.rect.height // 2, SCREEN_HEIGHT - self.rect.height // 2)
        self.direction_x = random.choice([1, -1])
        self.direction_y = random.choice([1, -1])
        self.speed = 3  # Initial speed
        self.moving = False  # Ball is stationary initially

    def start_moving(self):
        self.moving = True  # Ball starts moving after first collision

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def intro_screen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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

# Main game loop
def main_game(mode):
    player1 = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, BLACK)
    player2 = Player(3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, WHITE)
    ball = Ball('ball.png') 
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1, ball)
    if mode == 2:
        all_sprites.add(player2)

    score_left = 0
    score_right = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get pressed keys
        keys = pygame.key.get_pressed()
        player1.update(keys, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
        if mode == 2:
            player2.update(keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

        # Ball movement and collision detection
        scores = ball.move(ball, player1, player2)
        score_left += scores[0]
        score_right += scores[1]

        # Render game elements
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        # Draw score
        screen.blit(font.render(str(score_left), False, WHITE), (150, 10))
        screen.blit(font.render(str(score_right), False, WHITE), (300, 10))

        # Check for game over
        if score_left == 11 or score_right == 11:
            return score_left, score_right

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Run the intro screen and start the game
game_mode = intro_screen()
main_game(game_mode)
