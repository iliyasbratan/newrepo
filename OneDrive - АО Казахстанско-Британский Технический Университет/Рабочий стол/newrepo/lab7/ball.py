import pygame

pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Параметры шара
radius = 25
x, y = WIDTH // 2, HEIGHT // 2
speed = 20

running = True
while running:
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (x, y), radius)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and y - radius - speed >= 0:
                y -= speed
            elif event.key == pygame.K_DOWN and y + radius + speed <= HEIGHT:
                y += speed
            elif event.key == pygame.K_LEFT and x - radius - speed >= 0:
                x -= speed
            elif event.key == pygame.K_RIGHT and x + radius + speed <= WIDTH:
                x += speed

pygame.quit()
