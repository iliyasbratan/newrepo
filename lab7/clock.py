import pygame, sys, datetime
import pygame.locals
import os


def calc_deg_from_sec(seconds):
  seconds %= 60
  return seconds * 6  # / 60 * 360


def calc_deg_from_min(minutes):
  minutes %= 60
  return minutes * 6  # / 60 * 360


def calc_deg_from_hours(hours):
  hours %= 12
  return hours * 30  # / 12 * 360


def blit_rotate(image, deg, pos, origin_pos):
    image_rect = image.get_rect(topleft = (pos[0] - origin_pos[0], pos[1]-origin_pos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-deg)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, deg)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    DISPLAYSURF.blit(rotated_image, rotated_image_rect)  

WIDTH = 800
HEIGHT = 600
CX = WIDTH // 2
CY = HEIGHT // 2
FPS = 30

pygame.init()
pygame.display.set_caption("MickiClock")

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
Frame = pygame.time.Clock()

clock_image = pygame.transform.scale(
  pygame.image.load("lab7/clock.png").convert_alpha(),
  (WIDTH, HEIGHT)
)
min_hand_image = pygame.image.load("lab7/minutes.png").convert_alpha()
sec_hand_image = pygame.image.load("lab7/seconds.png").convert_alpha()

INITIAL_MIN_HAND_ANGLE = 310
min_hand_angle = 0
INITIAL_SEC_HAND_ANGLE = 58
sec_hand_angle = 0
SPEED = 1
while True:
  for event in pygame.event.get():
    if event.type == pygame.locals.QUIT:
      pygame.quit()
      sys.exit()
  
  # min_hand_angle = -calc_deg_from_min(
  #   (datetime.datetime.now().minute + datetime.datetime.now().second / 60) * SPEED
  # )
  # sec_hand_angle = -calc_deg_from_sec(
  #   (datetime.datetime.now().second + datetime.datetime.now().microsecond / 1000000) * SPEED
  # )

  min_hand_angle = -calc_deg_from_hours(
    (datetime.datetime.now().hour + datetime.datetime.now().minute / 60) * SPEED
  )
  sec_hand_angle = -calc_deg_from_min(
    (datetime.datetime.now().minute + datetime.datetime.now().second / 60) * SPEED
  )


  DISPLAYSURF.blit(clock_image, (0, 0))
  blit_rotate(min_hand_image, INITIAL_MIN_HAND_ANGLE + min_hand_angle, (CX, CY), (CX, CY))
  blit_rotate(sec_hand_image, INITIAL_SEC_HAND_ANGLE + sec_hand_angle, (CX, CY), (CX, CY))

  pygame.display.update()

  Frame.tick(FPS)