import pygame
import random
import sys
import json
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Platformer by Vishisht")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Files
SCORES_FILE = "scores.json"

# Load / Save scores
def load_scores():
    if not os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "w") as f:
            json.dump({}, f)
    with open(SCORES_FILE, "r") as f:
        return json.load(f)

def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)

# Sounds
jump_sound = pygame.mixer.Sound("assets/jump.wav")
coin_sound = pygame.mixer.Sound("assets/coin.wav")
gameover_sound = pygame.mixer.Sound("assets/gameover.wav")

# Fonts
font = pygame.font.SysFont("comicsans", 30)

# Player settings
player_width, player_height = 50, 50
player_speed = 5
jump_strength = -15
gravity = 0.8

# Load player images for animation
player_images = [pygame.image.load(f"assets/player{frame}.png") for frame in range(1,3)]

# Load enemy images for animation
enemy_images = [pygame.image.load(f"assets/enemy{frame}.png") for frame in range(1,3)]

# Level data
levels = [
    {  # Level 1
        "background": "assets/background1.png",
        "platforms": [{"rect": (0, HEIGHT-40, WIDTH, 40), "vel":0},
                      {"rect": (200,450,150,20), "vel":1}],
        "coins": [(230,400,20,20),(430,300,20,20)],
        "enemies": [{"rect":(600,400,40,40),"vel":2}]
    },
    {  # Level 2
        "background": "assets/background2.png",
        "platforms": [{"rect": (0, HEIGHT-40, WIDTH, 40), "vel":0},
                      {"rect": (150,500,150,20), "vel":1},
                      {"rect": (350,400,150,20), "vel":-1}],
        "coins": [(180,450,20,20),(380,350,20,20),(580,250,20,20)],
        "enemies": [{"rect":(250,460,40,40),"vel":2}, {"rect":(450,360,40,40),"vel":-2}]
    }
]

# Draw all objects
def draw_window(player_rect, platforms, coins, enemies, score, level_index, frame):
    bg = pygame.image.load(levels[level_index]["background"]).convert()
    win.blit(bg, (0,0))

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(win, (0,255,0), plat["rect"])

    # Draw coins
    for coin in coins:
        pygame.draw.rect(win, YELLOW, coin)

    # Draw enemies
    for i, enemy in enumerate(enemies):
        img = enemy_images[frame % len(enemy_images)]
        win.blit(img, enemy["rect"])

    # Draw player
    img = player_images[frame % len(player_images)]
    win.blit(img, player_rect)

    # Draw score
    score_text = font.render(f"Score: {score}  Level: {level_index+1}", True, BLACK)
    win.blit(score_text, (10,10))

    # Draw leaderboard top 3
    scores = load_scores()
    top_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    y_offset = 50
    for name, s in top_scores:
        lb_text = font.render(f"{name}: {s}", True, BLACK)
        win.blit(lb_text, (10, y_offset))
        y_offset += 30

    pygame.display.update()

# Main game function
def main():
    username = input("Enter your name: ").strip()
    scores = load_scores()
    if username not in scores:
        scores[username] = 0

    level_index = 0
    score = scores[username]

    while level_index < len(levels):
        level = levels[level_index]

        # Player start
        player_x, player_y = 100, HEIGHT - player_height - 50
        player_vel_x, player_vel_y = 0, 0
        on_ground = False

        # Create platform rects with velocity
        platform_rects = [{"rect":pygame.Rect(*plat["rect"]),"vel":plat["vel"]} for plat in level["platforms"]]

        # Coins
        coin_rects = [pygame.Rect(*coin) for coin in level["coins"]]

        # Enemies
        enemy_rects = [{"rect":pygame.Rect(*enemy["rect"]),"vel":enemy["vel"]} for enemy in level["enemies"]]

        frame = 0
        run = True
        while run:
            clock.tick(FPS)
            frame +=1

            # Gravity
            player_vel_y += gravity
            player_x += player_vel_x
            player_y += player_vel_y
            on_ground = False
            player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

            # Collision with platforms
            for plat in platform_rects:
                rect = plat["rect"]
                if player_rect.colliderect(rect) and player_vel_y >=0:
                    player_y = rect.top - player_height
                    player_vel_y = 0
                    on_ground = True

                # Moving platforms
                if plat["vel"] !=0:
                    rect.x += plat["vel"]
                    if rect.left <0 or rect.right > WIDTH:
                        plat["vel"] *= -1

            # Collect coins
            for coin in coin_rects[:]:
                if player_rect.colliderect(coin):
                    coin_rects.remove(coin)
                    score +=10
                    pygame.mixer.Sound.play(coin_sound)

            # Move enemies
            for enemy in enemy_rects:
                rect = enemy["rect"]
                rect.x += enemy["vel"]
                if rect.left <0 or rect.right > WIDTH:
                    enemy["vel"] *= -1
                if player_rect.colliderect(rect):
                    pygame.mixer.Sound.play(gameover_sound)
                    print("Game Over! Final Score:", score)
                    scores[username] = score
                    save_scores(scores)
                    return

            # Check fall
            if player_y > HEIGHT:
                pygame.mixer.Sound.play(gameover_sound)
                print("Game Over! Final Score:", score)
                scores[username] = score
                save_scores(scores)
                return

            draw_window(player_rect, platform_rects, coin_rects, enemy_rects, score, level_index, frame)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    scores[username] = score
                    save_scores(scores)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_vel_x = -player_speed
                    if event.key == pygame.K_RIGHT:
                        player_vel_x = player_speed
                    if event.key == pygame.K_SPACE and on_ground:
                        player_vel_y = jump_strength
                        pygame.mixer.Sound.play(jump_sound)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player_vel_x <0:
                        player_vel_x = 0
                    if event.key == pygame.K_RIGHT and player_vel_x >0:
                        player_vel_x =0

            # Check level complete
            if not coin_rects:
                level_index +=1
                run = False

    print("Congratulations! You completed all levels!")
    print("Final Score:", score)
    scores[username] = score
    save_scores(scores)
    pygame.quit()

if __name__ == "__main__":
    main()
