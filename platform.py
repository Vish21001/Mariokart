import pygame
import random

# Initialize pygame
pygame.init()

# Screen
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game by Vishisht")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player
player_width = 50
player_height = 50
player_x = 100
player_y = HEIGHT - player_height - 50
player_vel_x = 0
player_vel_y = 0
player_speed = 5
jump_strength = -15
gravity = 0.8
on_ground = False

# Platforms
platforms = [
    pygame.Rect(0, HEIGHT - 40, WIDTH, 40),  # ground
    pygame.Rect(200, 450, 150, 20),
    pygame.Rect(400, 350, 150, 20),
    pygame.Rect(600, 250, 150, 20)
]

# Coins
coins = [pygame.Rect(230, 400, 20, 20), pygame.Rect(430, 300, 20, 20), pygame.Rect(630, 200, 20, 20)]
score = 0

# Font
font = pygame.font.SysFont("comicsans", 30)

# Draw everything
def draw_window():
    win.fill(WHITE)
    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(win, GREEN, plat)
    # Draw player
    pygame.draw.rect(win, BLUE, (player_x, player_y, player_width, player_height))
    # Draw coins
    for coin in coins:
        pygame.draw.rect(win, YELLOW, coin)
    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    win.blit(score_text, (10, 10))
    pygame.display.update()

# Main loop
run = True
while run:
    clock.tick(FPS)
    player_vel_y += gravity
    player_x += player_vel_x
    player_y += player_vel_y
    on_ground = False

    # Collision with platforms
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for plat in platforms:
        if player_rect.colliderect(plat) and player_vel_y >=0:
            player_y = plat.top - player_height
            player_vel_y = 0
            on_ground = True

    # Collect coins
    for coin in coins[:]:
        if player_rect.colliderect(coin):
            coins.remove(coin)
            score += 10

    # Check fall
    if player_y > HEIGHT:
        print("Game Over! Final Score:", score)
        run = False

    draw_window()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_vel_x = -player_speed
            if event.key == pygame.K_RIGHT:
                player_vel_x = player_speed
            if event.key == pygame.K_SPACE and on_ground:
                player_vel_y = jump_strength
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player_vel_x < 0:
                player_vel_x = 0
            if event.key == pygame.K_RIGHT and player_vel_x > 0:
                player_vel_x = 0

pygame.quit()
