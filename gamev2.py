import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1200

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Eat or Be Eaten")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_radius = 2
player_speed = 5

# Enemy settings
green_enemies = []
red_enemies = []
num_green_enemies = 10
num_red_enemies = 5
enemy_radius = 1

# Enemy directions, states, and energy
green_directions = []
red_directions = []
last_run_time = {}  # Track when green enemies start running
green_energy = [50 for _ in range(num_green_enemies)]
red_energy = [50 for _ in range(num_red_enemies)]

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

def initialize_enemy_directions(num_enemies):
    """Assign random initial directions to each enemy."""
    return [[random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])] for _ in range(num_enemies)]

def distance(pos1, pos2):
    """Calculate the distance between two points."""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def move_enemy(enemy_pos, direction, speed=2):
    """Move enemy in assigned direction and bounce off walls."""
    enemy_pos[0] += direction[0] * speed
    enemy_pos[1] += direction[1] * speed

    # Bounce off walls
    if enemy_pos[0] <= enemy_radius or enemy_pos[0] >= SCREEN_WIDTH - enemy_radius:
        direction[0] = -direction[0]
    if enemy_pos[1] <= enemy_radius or enemy_pos[1] >= SCREEN_HEIGHT - enemy_radius:
        direction[1] = -direction[1]

def chase_enemy(enemy_pos, target_pos, speed=3):
    """Move enemy towards the player aggressively."""
    dx = target_pos[0] - enemy_pos[0]
    dy = target_pos[1] - enemy_pos[1]
    dist = math.sqrt(dx**2 + dy**2)
    if dist > 0:
        enemy_pos[0] += (dx / dist) * speed
        enemy_pos[1] += (dy / dist) * speed

def flee_enemy(enemy_pos, target_pos, direction, speed=4):
    """Move enemy away from the player for fleeing behavior."""
    dx = enemy_pos[0] - target_pos[0]
    dy = enemy_pos[1] - target_pos[1]
    dist = math.sqrt(dx**2 + dy**2)
    if dist > 0:
        enemy_pos[0] += (dx / dist) * speed
        enemy_pos[1] += (dy / dist) * speed

def update_energy(energy_list, index, running_fast):
    """Update enemy energy levels based on running behavior."""
    if energy_list[index] <= 0:  # If energy is depleted, rest
        energy_list[index] += 10 / FPS  # Regain energy
        return "resting"
    elif running_fast:  # Running fast consumes more energy
        energy_list[index] -= 10 / FPS
        return "running_fast"
    else:  # Running slowly consumes less energy
        energy_list[index] -= 5 / FPS
        return "running_slow"

# Create enemies
green_enemies = [create_enemy() for _ in range(num_green_enemies)]
red_enemies = [create_enemy() for _ in range(num_red_enemies)]
green_directions = initialize_enemy_directions(num_green_enemies)
red_directions = initialize_enemy_directions(num_red_enemies)

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
    current_time = time.time()
    for i, enemy in enumerate(green_enemies):
        enemy_key = i  # Use the index as the key
        if distance(enemy, player_pos) < 150 and green_energy[i] > 0:  # Flee if player is close
            state = update_energy(green_energy, i, running_fast=True)
            if state == "running_fast":
                flee_enemy(enemy, player_pos, green_directions[i], speed=4)
            else:
                pygame.draw.circle(screen, YELLOW, enemy, enemy_radius, 0)  # Resting indicator
        else:
            state = update_energy(green_energy, i, running_fast=False)
            if state == "resting":
                pygame.draw.circle(screen, YELLOW, enemy, enemy_radius, 0)  # Resting
            else:
                move_enemy(enemy, green_directions[i], speed=2)
        pygame.draw.circle(screen, GREEN, enemy, enemy_radius, 0)

    # Move and draw red enemies
    for i, enemy in enumerate(red_enemies):
        if distance(enemy, player_pos) < 200 and red_energy[i] > 0:  # Aggressively chase player
            state = update_energy(red_energy, i, running_fast=True)
            if state == "running_fast":
                chase_enemy(enemy, player_pos, speed=4)
            else:
                pygame.draw.circle(screen, YELLOW, enemy, enemy_radius, 0)  # Resting indicator
        else:
            state = update_energy(red_energy, i, running_fast=False)
            if state == "resting":
                pygame.draw.circle(screen, YELLOW, enemy, enemy_radius, 0)
            else:
                move_enemy(enemy, red_directions[i], speed=2)
        pygame.draw.circle(screen, RED, enemy, enemy_radius, 0)

    # Check collisions with green enemies
    for i, enemy in enumerate(green_enemies[:]):
        if distance(player_pos, enemy) < player_radius + enemy_radius:
            green_enemies.pop(i)
            green_directions.pop(i)
            green_energy.pop(i)
            score += 1

    # Check collisions with red enemies
    for enemy in red_enemies:
        if distance(player_pos, enemy) < player_radius + enemy_radius:
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
