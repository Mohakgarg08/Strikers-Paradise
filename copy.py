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

# This is setting the screensssss
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Striker's Paradise")

# Load and scale background image
background_image = pygame.image.load('Strikers-Paradise/Images/Field.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load logo image
logo_image = pygame.image.load('Strikers-Paradise/Images/Logo.png')

# Define player lines for 4-3-2-1 formation
player1_lines = [100, 200, 300, 400]  # Example y-coordinates for player1 lines
player2_lines = [100, 200, 300, 400]  # Example y-coordinates for player2 lines

# Define player x-coordinates for 4-3-2-1 formation
player1_x_positions = [
    [50, 150, 250, 350],  # 4 players
    [100, 200, 300],      # 3 players
    [150, 250],           # 2 players
    [200]                 # 1 player
]
player2_x_positions = [
    [SCREEN_WIDTH - 50, SCREEN_WIDTH - 150, SCREEN_WIDTH - 250, SCREEN_WIDTH - 350],  # 4 players
    [SCREEN_WIDTH - 100, SCREEN_WIDTH - 200, SCREEN_WIDTH - 300],                    # 3 players
    [SCREEN_WIDTH - 150, SCREEN_WIDTH - 250],                                        # 2 players
    [SCREEN_WIDTH - 200]                                                             # 1 player
]

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # Smaller player size
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PLAYER_SPEED

    def update(self, keys, up_key, down_key):
        if keys[up_key]:
            self.rect.y -= self.speed
        if keys[down_key]:
            self.rect.y += self.speed
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))  # Keep player within screen bounds

# Define ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self, ball, players1, players2):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Collision with top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

        # Collision with players
        enlarged_rect = self.rect.inflate(10, 10)  # Increase the collision area by 10 pixels in both width and height
        for player in players1 + players2:
            if enlarged_rect.colliderect(player.rect):
                self.speed_x *= -1

        # Scoring
        score_left = 0
        score_right = 0
        if self.rect.left <= 0:
            score_right = 1
            self.rect.x = SCREEN_WIDTH // 2
            self.rect.y = SCREEN_HEIGHT // 2
        if self.rect.right >= SCREEN_WIDTH:
            score_left = 1
            self.rect.x = SCREEN_WIDTH // 2
            self.rect.y = SCREEN_HEIGHT // 2

        return score_left, score_right

# Create player instances for 4-3-2-1 formation
players1 = []
players2 = []

# Create players for player1
for i, y in enumerate(player1_lines):
    for x in player1_x_positions[i]:
        player = Player(x, y)
        players1.append(player)

# Create players for player2
for i, y in enumerate(player2_lines):
    for x in player2_x_positions[i]:
        player = Player(x, y)
        players2.append(player)

# Create ball instance
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(*players1)
all_sprites.add(*players2)
all_sprites.add(ball)

# Game loop
running = True
score_left = 0
score_right = 0
mode = 2  # Assuming mode 2 is for two players
player1_selected_line = 0
player2_selected_line = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Switch selected line for player1
    if keys[pygame.K_a] and player1_selected_line > 0:
        player1_selected_line -= 1
    if keys[pygame.K_d] and player1_selected_line < 3:
        player1_selected_line += 1

    # Switch selected line for player2
    if mode == 2:
        if keys[pygame.K_LEFT] and player2_selected_line > 0:
            player2_selected_line -= 1
        if keys[pygame.K_RIGHT] and player2_selected_line < 3:
            player2_selected_line += 1

    # Update player1 positions
    for i, player in enumerate(players1):
        if i // (4 - i % 4) == player1_selected_line:
            for p in players1:
                if p.rect.x == player.rect.x:
                    p.update(keys, pygame.K_w, pygame.K_s)

    # Update player2 positions
    if mode == 2:
        for i, player in enumerate(players2):
            if i // (4 - i % 4) == player2_selected_line:
                for p in players2:
                    if p.rect.x == player.rect.x:
                        p.update(keys, pygame.K_UP, pygame.K_DOWN)

    # Ball movement and collision detection
    scores = ball.move(ball, players1, players2)
    score_left += scores[0]
    score_right += scores[1]

    # Render game elements
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    # Draw score
    font = pygame.font.Font(None, 74)
    text = font.render(str(score_left), 1, (255, 255, 255))
    screen.blit(text, (250, 10))
    text = font.render(str(score_right), 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 250, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

pygame.quit()
sys.exit()