import pygame, sys
import random

# Initialize Pygame
pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 30
PLAYER_SPEED = 7  # Increased player speed for smoother and faster movement
BALL_SPEED_X = 5  # Slower ball speed on the x-axis
BALL_SPEED_Y = 5  # Slower ball speed on the y-axis

# This is setting the screensssss
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Striker's Paradise")

# Load and scale background image
background_image = pygame.image.load('Images\Field.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load logo image
logo_image = pygame.image.load('Images/Logo.png')
logo_image = pygame.transform.scale(logo_image, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

# Load player images
player1_image = pygame.image.load('Images\characterBlue.png')
player2_image = pygame.image.load('Images\characterRed.png')
ball_image = pygame.image.load('Images\Ball.png')

# Load score sound
score_sound = pygame.mixer.Sound('Audio/stadium-crowd-cheer-noise-loud_77bpm.wav')

# Define player y-coordinates for 4-3-2-1 formation
player1_y_positions = [
    [100, 200, 300, 400],  # 4 players in defense
    [150, 250, 350],       # 3 players in midfield
    [200, 300],            # 2 players in attack
    [250]                  # 1 player in forward
]
player2_y_positions = [
    [100, 200, 300, 400],  # 4 players in defense
    [150, 250, 350],       # 3 players in midfield
    [200, 300],            # 2 players in attack
    [250]                  # 1 player in forward
]

# Define player x-coordinates for 4-3-2-1 formation
player1_x_positions = [50, 150, 250, 350]
player2_x_positions = [SCREEN_WIDTH - 50, SCREEN_WIDTH - 150, SCREEN_WIDTH - 250, SCREEN_WIDTH - 350]

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (30, 30))  # Scale player image to fit the player size
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PLAYER_SPEED

    def move_up(self):
        self.rect.y -= self.speed
        self.rect.y = max(0, self.rect.y)

    def move_down(self):
        self.rect.y += self.speed
        self.rect.y = min(SCREEN_HEIGHT - self.rect.height, self.rect.y)

# Define ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y,image):
        super().__init__()
        self.image = pygame.transform.scale(image, (20, 20))  # Scale player image to fit the player size
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self, players1, players2):
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
            pygame.mixer.Sound.play(score_sound)  # Play score sound
        if self.rect.right >= SCREEN_WIDTH:
            score_left = 1
            self.rect.x = SCREEN_WIDTH // 2
            self.rect.y = SCREEN_HEIGHT // 2
            pygame.mixer.Sound.play(score_sound)  # Play score sound

        return score_left, score_right

# Create player instances for 4-3-2-1 formation
players1 = []
players2 = []

# Create players for player1 (using player1_image)
for i, x in enumerate(player1_x_positions):
    for y in player1_y_positions[i]:
        player = Player(x, y, player1_image)
        players1.append(player)

# Create players for player2 (using player2_image)
for i, x in enumerate(player2_x_positions):
    for y in player2_y_positions[i]:
        player = Player(x, y, player2_image)
        players2.append(player)

# Create ball instance
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, ball_image)

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
player1_selected_formation = 0
player2_selected_formation = 0
total_formations = 4  # Assuming there are 4 formations

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Switch selected formation for player1
            if event.key == pygame.K_a:
                player1_selected_formation -= 1
                if player1_selected_formation < 0:
                    player1_selected_formation = total_formations - 1
                print(f"Player 1 selected formation: {player1_selected_formation}")
            elif event.key == pygame.K_d:
                player1_selected_formation += 1
                if player1_selected_formation >= total_formations:
                    player1_selected_formation = 0
                print(f"Player 1 selected formation: {player1_selected_formation}")

            # Switch selected formation for player2
            if mode == 2:
                if event.key == pygame.K_RIGHT:
                    player2_selected_formation -= 1
                    if player2_selected_formation < 0:
                        player2_selected_formation = total_formations - 1
                    print(f"Player 2 selected formation: {player2_selected_formation}")
                elif event.key == pygame.K_LEFT:
                    player2_selected_formation += 1
                    if player2_selected_formation >= total_formations:
                        player2_selected_formation = 0
                    print(f"Player 2 selected formation: {player2_selected_formation}")

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Update player1 positions
    for player in players1:
        if player.rect.x == player1_x_positions[player1_selected_formation]:
            if keys[pygame.K_w]:
                player.move_up()
            if keys[pygame.K_s]:
                player.move_down()

    # Update player2 positions
    if mode == 2:
        for player in players2:
            if player.rect.x == player2_x_positions[player2_selected_formation]:
                if keys[pygame.K_UP]:
                    player.move_up()
                if keys[pygame.K_DOWN]:
                    player.move_down()

    # Ball movement and collision detection
    scores = ball.move(players1, players2)
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
    screen.blit(text, (420, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

pygame.quit()
sys.exit()