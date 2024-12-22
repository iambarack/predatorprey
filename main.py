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
player_radius = 5
player_speed = 5

# Enemy settings
green_enemies = []
red_enemies = []
num_green_enemies = 10
num_red_enemies = 5
enemy_radius = 5

# Enemy directions, states, and energy
green_directions = []
red_directions = []
green_energy = [100 for _ in range(num_green_enemies)]
red_energy = [100 for _ in range(num_red_enemies)]

# Enemy speeds
ENEMY_SPEEDS = {
    "idle": 0,
    "walk": 1,
    "run": 3,
    "lifeordeath": 5
}

def draw_text(surface, text, position, color=WHITE):
    """Utility function to draw text on the screen."""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

# Font
font = pygame.font.Font(None, 36)

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
    """Move enemy in assigned direction and keep within bounds."""
    enemy_pos[0] += direction[0] * speed
    enemy_pos[1] += direction[1] * speed
    enemy_pos[0] = max(min(enemy_pos[0], SCREEN_WIDTH - enemy_radius), enemy_radius)
    enemy_pos[1] = max(min(enemy_pos[1], SCREEN_HEIGHT - enemy_radius), enemy_radius)

def update_energy(energy_list, index, state):
    """Update energy based on state."""
    if state == "idle":
        energy_list[index] = min(100, energy_list[index] + 20 / FPS)
    elif state == "walk":
        energy_list[index] = min(100, energy_list[index] + 10 / FPS)
    elif state == "run":
        energy_list[index] -= 10 / FPS
    elif state == "lifeordeath":
        energy_list[index] -= 20 / FPS

def decide_state(energy, dist_to_player):
    """Decide the state based on energy and player distance."""
    if energy <= 0:
        return "idle"
    elif dist_to_player < 100:
        return "lifeordeath"
    elif dist_to_player < 200:
        return "run"
    else:
        return "walk"

def chase_enemy(enemy_pos, target_pos, speed):
    """Move enemy towards the player aggressively."""
    dx = target_pos[0] - enemy_pos[0]
    dy = target_pos[1] - enemy_pos[1]
    dist = max(1, math.sqrt(dx**2 + dy**2))
    enemy_pos[0] += (dx / dist) * speed
    enemy_pos[1] += (dy / dist) * speed

def flee_enemy(enemy_pos, target_pos, speed):
    """Move enemy away from the player."""
    dx = enemy_pos[0] - target_pos[0]
    dy = enemy_pos[1] - target_pos[1]
    dist = max(1, math.sqrt(dx**2 + dy**2))
    enemy_pos[0] += (dx / dist) * speed
    enemy_pos[1] += (dy / dist) * speed

green_enemies = [create_enemy() for _ in range(num_green_enemies)]
red_enemies = [create_enemy() for _ in range(num_red_enemies)]
green_directions = initialize_enemy_directions(num_green_enemies)
red_directions = initialize_enemy_directions(num_red_enemies)

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]: player_pos[1] += player_speed
    if keys[pygame.K_LEFT]: player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]: player_pos[0] += player_speed
    player_pos[0] = max(min(player_pos[0], SCREEN_WIDTH - player_radius), player_radius)
    player_pos[1] = max(min(player_pos[1], SCREEN_HEIGHT - player_radius), player_radius)
    pygame.draw.circle(screen, BLUE, player_pos, player_radius)

    # Green enemies
    for i, enemy in enumerate(green_enemies):
        dist = distance(enemy, player_pos)
        state = decide_state(green_energy[i], dist)
        update_energy(green_energy, i, state)
        if state == "lifeordeath":
            flee_enemy(enemy, player_pos, ENEMY_SPEEDS[state])
        elif state == "run":
            flee_enemy(enemy, player_pos, ENEMY_SPEEDS[state])
        else:
            move_enemy(enemy, green_directions[i], ENEMY_SPEEDS[state])
        color = GREEN if state != "idle" else YELLOW
        pygame.draw.circle(screen, color, enemy, enemy_radius)

    # Red enemies
    for i, enemy in enumerate(red_enemies):
        dist = distance(enemy, player_pos)
        state = decide_state(red_energy[i], dist)
        update_energy(red_energy, i, state)
        if state == "lifeordeath" or state == "run":
            chase_enemy(enemy, player_pos, ENEMY_SPEEDS[state])
        else:
            move_enemy(enemy, red_directions[i], ENEMY_SPEEDS[state])
        color = RED if state != "idle" else YELLOW
        pygame.draw.circle(screen, color, enemy, enemy_radius)

    pygame.draw.circle(screen, BLUE, player_pos, player_radius)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
