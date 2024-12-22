import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Eat or Be Eaten")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_radius = 10
player_speed = 5

# Enemy settings
green_enemies = []
red_enemies = []
num_green_enemies = 10
num_red_enemies = 5
enemy_radius = 5

# Score
score = 0

# Font
font = pygame.font.Font(None, 36)

def draw_text(surface, text, position, color=WHITE):
    """Utility function to draw text on the screen."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def create_enemy():
    """Create a random enemy position within screen bounds."""
    x = random.randint(enemy_radius, SCREEN_WIDTH - enemy_radius)
    y = random.randint(enemy_radius, SCREEN_HEIGHT - enemy_radius)
    return [x, y]

def move_enemy(enemy_pos):
    """Move enemy randomly within bounds."""
    enemy_pos[0] += random.randint(-2, 2)
    enemy_pos[1] += random.randint(-2, 2)

    # Keep enemy within screen bounds
    enemy_pos[0] = max(enemy_radius, min(SCREEN_WIDTH - enemy_radius, enemy_pos[0]))
    enemy_pos[1] = max(enemy_radius, min(SCREEN_HEIGHT - enemy_radius, enemy_pos[1]))

def is_collision(pos1, pos2, radius1, radius2):
    """Check if two circles collide."""
    distance = math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
    return distance < radius1 + radius2

# Create enemies
green_enemies = [create_enemy() for _ in range(num_green_enemies)]
red_enemies = [create_enemy() for _ in range(num_red_enemies)]

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen with black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed

    # Keep player within screen bounds
    player_pos[0] = max(player_radius, min(SCREEN_WIDTH - player_radius, player_pos[0]))
    player_pos[1] = max(player_radius, min(SCREEN_HEIGHT - player_radius, player_pos[1]))

    # Draw player
    pygame.draw.circle(screen, BLUE, player_pos, player_radius, 0)

    # Move and draw green enemies
    for enemy in green_enemies:
        move_enemy(enemy)
        pygame.draw.circle(screen, GREEN, enemy, enemy_radius, 0)

    # Move and draw red enemies
    for enemy in red_enemies:
        move_enemy(enemy)
        pygame.draw.circle(screen, RED, enemy, enemy_radius, 0)

    # Check collisions with green enemies
    for enemy in green_enemies[:]:
        if is_collision(player_pos, enemy, player_radius, enemy_radius):
            green_enemies.remove(enemy)
            score += 1

    # Check collisions with red enemies
    for enemy in red_enemies:
        if is_collision(player_pos, enemy, player_radius, enemy_radius):
            running = False  # End game

    # Draw score
    draw_text(screen, f"Score: {score}", (10, 10))

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Game over screen
screen.fill((0, 0, 0))
draw_text(screen, "Game Over", (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20), color=RED)
draw_text(screen, f"Final Score: {score}", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))
pygame.display.flip()

# Wait before exiting
pygame.time.wait(3000)
pygame.quit()
