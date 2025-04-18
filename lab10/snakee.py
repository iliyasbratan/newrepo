import pygame
import random
import sys
import time
import psycopg2

# === POSTGRESQL SETUP ===
def connect_to_db():
    return psycopg2.connect(
        host="localhost",
          
        user="postgres",
        password="12345678" 
    )
def get_user_id(username):
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            if user:
                return user[0]
            else:
                cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
                new_id = cur.fetchone()[0]
                conn.commit()
                return new_id

def load_progress(user_id):
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT score, level 
                FROM user_score 
                WHERE user_id = %s 
                ORDER BY saved_at DESC 
                LIMIT 1
            """, (user_id,))
            row = cur.fetchone()
            if row:
                return row
            else:
                return 0, 0

def save_progress(user_id, score, level):
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO user_score (user_id, score, level)
                VALUES (%s, %s, %s)
            """, (user_id, score, level))
            conn.commit()
    print(f"Прогресс сохранён: user_id={user_id}, score={score}, level={level}")

# === CONSTANTS ===
USERNAME = input("Введите ваше имя: ")
USER_ID = get_user_id(USERNAME)
score, level = load_progress(USER_ID)

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (80, 80, 80)
YELLOW = (255, 255, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# === LEVEL AND WALLS ===
def get_level(score):
    if score < 5:
        return 0
    elif score < 10:
        return 1
    else:
        return 2

def get_speed(level):
    if level == 0:
        return 8
    elif level == 1:
        return 12
    else:
        return 15

def get_walls_for_level(level):
    walls = set()
    if level >= 0:
        for x in range(GRID_WIDTH):
            walls.add((x, 0))
            walls.add((x, GRID_HEIGHT - 1))
        for y in range(GRID_HEIGHT):
            walls.add((0, y))
            walls.add((GRID_WIDTH - 1, y))

    if level >= 1:
        for i in range(5, 15):
            walls.add((i, i))

    if level >= 2:
        for i in range(10, 20):
            walls.add((i, GRID_HEIGHT - i))

    return walls

# === GAME VARIABLES ===
snake = [(5, 5)]
direction = (1, 0)
game_over = False

food = (0, 0)
food_timer = time.time()
FOOD_LIFETIME = 5
food_value = 1

def spawn_food():
    global food, food_value, food_timer
    while True:
        candidate = (
            random.randint(1, GRID_WIDTH - 2),
            random.randint(1, GRID_HEIGHT - 2)
        )
        if candidate not in walls and candidate not in snake:
            food = candidate
            break
    food_value = random.choice([1, 2, 3])
    food_timer = time.time()

level = get_level(score)
speed = get_speed(level)
walls = get_walls_for_level(level)
spawn_food()

# === DRAWING THE GAME ===
def draw_all():
    win.fill(GREEN)

    # Отображаем стены
    for wx, wy in walls:
        pygame.draw.rect(win, GRAY, (wx * CELL_SIZE, wy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отображаем еду
    pygame.draw.rect(win, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    txt = font.render(str(food_value), True, BLACK)
    win.blit(txt, (food[0] * CELL_SIZE + 5, food[1] * CELL_SIZE))

    # Отображаем змейку
    for sx, sy in snake:
        pygame.draw.rect(win, BLACK, (sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    s1 = font.render(f"User: {USERNAME}", True, WHITE)
    s2 = font.render(f"Score: {score}", True, WHITE)
    s3 = font.render(f"Level: {level}", True, WHITE)
    win.blit(s1, (10, 10))
    win.blit(s2, (10, 40))
    win.blit(s3, (10, 70))

    pygame.display.update()

# === MAIN GAME LOOP ===
while True:
    clock.tick(speed)

    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_progress(USER_ID, score, level)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_p:  # Pause game
                    save_progress(USER_ID, score, level)
                    print("Game paused! Progress saved.")

        head = snake[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        if new_head in snake or new_head in walls:
            game_over = True
        else:
            snake.insert(0, new_head)
            if new_head == food:
                score += food_value
                spawn_food()
                new_level = get_level(score)
                if new_level != level:
                    level = new_level
                    speed = get_speed(level)
                    walls = get_walls_for_level(level)
            else:
                snake.pop()

        # Update screen
        draw_all()

    else:
        # Game Over screen
        win.fill(BLACK)
        go_text = font.render("Game Over! Press R to Restart", True, YELLOW)
        win.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_progress(USER_ID, score, level)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    snake = [(5, 5)]
                    direction = (1, 0)
                    score, level = 0, 0
                    speed = get_speed(level)
                    walls = get_walls_for_level(level)
                    spawn_food()
                    game_over = False
