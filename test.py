import bullet_class
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 458), 0, 32)
pygame.display.set_caption("子弹测试")

background = pygame.image.load("84.jpg").convert_alpha()
clock = pygame.time.Clock()

bullet_group = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    time_passed = clock.tick(60)
    time_passed_second = time_passed / 1000.
    current_time = pygame.time.get_ticks() / 1000

    pressed_mouse = pygame.mouse.get_pressed()
    if pressed_mouse[0]:
        mouse_pos = pygame.mouse.get_pos()
        bullet = bullet_class.OrdinaryBullet(screen)
        bullet.fired(mouse_pos[0], mouse_pos[1])
        bullet_group.add(bullet)

    for b in bullet_group.sprites():
        if b.loss():
            bullet_group.remove(b)

    screen.blit(background, (0, 0))
    bullet_group.update(current_time, time_passed_second, "up")
    bullet_group.draw(screen)
    pygame.display.update()
