import pygame
import os

pygame.init()


WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")


MUSIC_DIR = "musics"

# if there is no music program will end
if not os.path.isdir(MUSIC_DIR):
    pygame.quit()
    exit()

tracks = [f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")]
if not tracks:
    pygame.quit()
    exit()

current_track = 0

def play_music():
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, tracks[current_track]))
    pygame.mixer.music.play()

play_music()  

running = True
while running:
    screen.fill((30, 30, 30))  
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_s:  
                pygame.mixer.music.stop()
            elif event.key == pygame.K_RIGHT:  
                current_track = (current_track + 1) % len(tracks)
                play_music()
            elif event.key == pygame.K_LEFT:  
                current_track = (current_track - 1) % len(tracks)
                play_music()

pygame.quit()
