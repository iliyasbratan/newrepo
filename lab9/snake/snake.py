import os
import pygame, json, random
from game_objects import Player, Food, Wall

# Загрузка цветов из файла
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'color.json')
with open(file_path) as f:
    color = json.loads(f.read())

pygame.init()

# Установка размеров окна
h = w = 400
win = pygame.display.set_mode((w, h))
pygame.display.set_caption('Snake')

# Функция для отрисовки текста с прозрачным фоном
def add_transparent_text(main_surface, text, size, x, y):
    font = pygame.font.SysFont('comicsansms', size)
    text = font.render(text, True, color['text'])
    surface = pygame.Surface((w,h))
    surface.fill(color['bg_color'])
    surface.blit(text, (0,0))
    surface.set_alpha(150)
    main_surface.blit(surface, (x, y))

# Функция для обновления фона
def fill_background(surface, level, balance, n_to_next_lvl):
    surface.fill(color['bg_color'])
    add_transparent_text(surface, f'LVL: {level}', 35, 0, 0)
    add_transparent_text(surface, f'Need: {balance}/{n_to_next_lvl}', 35, 200, 0)
    for i in range(0, w, 20):
        pygame.draw.line(surface, color['black'], (0, max(i-1, 0)), (w, max(i-1, 0)), 2)
        pygame.draw.line(surface, color['black'], (max(i-1, 0), 0), (max(i-1, 0), h), 2)

fill_background(win, 1, 0, 5)

LEVEL = 1
wall = Wall(level=LEVEL)
player = Player(wall.points)
food = Food(player.points + wall.points)
food_timer = 0  # Таймер для исчезновения еды
food_lifetime = random.randint(5, 10) * 1000  # Время жизни еды (в мс)

speed = 5
BALANCE = 0
N_to_next_lvl = 5
clock = pygame.time.Clock()
run = True
losed = None

while run:
    k_down_events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            k_down_events.append(event)
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER and losed is not None:
                wall = Wall(level=LEVEL)
                player = Player(wall.points)
                food = Food(player.points + wall.points)
                BALANCE = 0
                losed = None

    if losed is None:
        player.process_input(k_down_events)
        fill_background(win, LEVEL, BALANCE, N_to_next_lvl)
        
        # Проверяем столкновение со стеной
        bumped_to_wall = wall.can_go(player.points[0], player.dx, player.dy)
        if bumped_to_wall:
            losed = bumped_to_wall
        
        if losed is None:
            losed = player.move(w, h)
        
        # Проверка поедания еды
        if food.can_eat(player.points[0]):
            player.add(player.points[0])
            BALANCE += food.weight  # Учитываем вес еды
            food = Food(player.points + wall.points)  # Создаем новую еду
            food_timer = pygame.time.get_ticks()  # Обновляем таймер
            food_lifetime = random.randint(5, 10) * 1000  # Задаем новое время жизни еды
        
        # Проверяем, не истек ли срок жизни еды
        if pygame.time.get_ticks() - food_timer > food_lifetime:
            food = Food(player.points + wall.points)
            food_timer = pygame.time.get_ticks()
            food_lifetime = random.randint(5, 10) * 1000
        
        # Проверяем переход на новый уровень
        if BALANCE >= N_to_next_lvl:
            LEVEL += 1
            wall = Wall(LEVEL)
            player = Player(wall.points)
            speed = speed + 2 if LEVEL <= 3 else speed + 8
            N_to_next_lvl = 999 if LEVEL > 3 else N_to_next_lvl
            BALANCE = 0
            
        # Отрисовка объектов
        player.draw(win)
        food.draw(win)
        wall.draw(win)
    else:
        # Отрисовка сообщения о проигрыше
        font = pygame.font.SysFont('comicsansms', 80)
        text = font.render('You Lose', True, color['red'])
        win.blit(text, (30, 120))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()
