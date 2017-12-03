import prop_classes
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 458), 0, 32)
pygame.display.set_caption("道具测试")

background = pygame.image.load("84.jpg").convert_alpha()
clock = pygame.time.Clock()

prop_group = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    time_passed = clock.tick(60)
    current_time = pygame.time.get_ticks()

    pressed_mouse = pygame.mouse.get_pressed()
    if pressed_mouse[0]:
        mouse_pos = pygame.mouse.get_pos()
        prop = prop_classes.CoinProp(screen)
        prop.produce(mouse_pos[0], mouse_pos[1], current_time)
        prop_group.add(prop)

    for p in prop_group.sprites():
        if p.loss(current_time):
            prop_group.remove(p)

    screen.blit(background, (0, 0))
    prop_group.update(current_time)
    prop_group.draw(screen)
    pygame.display.update()
