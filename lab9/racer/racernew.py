import os
import pygame, sys
from pygame.locals import *
import random, time

# Initializing pygame
pygame.init()

# Setting up FPS
FPS = 120
FramePerSec = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SPEED_COIN = 5
SCORE = 0
Coin_score = 0
COINS_NEEDED = 5  # Coins required to increase speed

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load background
background = pygame.image.load(os.path.join(base_dir, 'images', 'street.png'))

# Create display surface
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

# Enemy and Coin class
class Enemy_and_Coin(pygame.sprite.Sprite):
    def __init__(self, coin=False, enemies=None):
        super().__init__()
        self.coin = coin
        self.weight = random.randint(1, 3) if coin else 0  # Weight for coins
        
        if not coin:
            self.image = pygame.image.load(os.path.join(base_dir, 'images', f"enemy{random.randint(1, 3)}.png"))
        else:
            self.image = pygame.image.load(os.path.join(base_dir, 'images', 'coin.png'))
        
        self.rect = self.image.get_rect()
        if not coin:
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
        else:
            self.coin_pos(enemies)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED if not self.coin else SPEED_COIN)
        if self.rect.top > SCREEN_HEIGHT:
            if not self.coin:
                self.image = pygame.image.load(os.path.join(base_dir, 'images', f"enemy{random.randint(1, 3)}.png"))
                SCORE += 1
                self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            else:
                self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), 0)
            self.rect.top = 0

    def coin_pos(self, enemies):
        self.rect.center = (random.randint(50, SCREEN_WIDTH-50), 0)
        while pygame.sprite.spritecollideany(self, enemies):
            self.rect.center = (random.randint(50, SCREEN_WIDTH-50), 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(base_dir, 'images', 'player.png'))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Create player, enemies, and coins
P1 = Player()
E1 = Enemy_and_Coin()
enemies = pygame.sprite.Group()
enemies.add(E1)

C1 = Enemy_and_Coin(True, enemies)
coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Speed increase event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == INC_SPEED:
            SPEED += 0.5

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    scores_coin = font_small.render(f'Coin: {Coin_score}', True, BLACK)
    DISPLAYSURF.blit(scores_coin, (310, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound(os.path.join(base_dir, 'sound', 'racer_sound.wav')).play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    
    # Coin collection logic
    for coin in coins:
        if pygame.sprite.collide_rect(P1, coin):
            Coin_score += coin.weight  # Increase score by coin weight
            coin.coin_pos(enemies)
            
            # Increase speed if N coins collected
            if Coin_score % COINS_NEEDED == 0:
                SPEED += 1
    
    pygame.display.update()
    FramePerSec.tick(FPS)
