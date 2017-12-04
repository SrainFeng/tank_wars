import pygame
from pygame.locals import *
from gameobjects.vector2 import Vector2
import bullet_classes, hinder_classes
from random import randint

pygame.init()
screen = pygame.display.set_mode((800, 458), 0, 32)
pygame.display.set_caption("碰撞测试")

background = pygame.image.load("84.jpg").convert_alpha()

clock = pygame.time.Clock()

# 创建一些精灵组
# 道具箱
boxes = pygame.sprite.Group()

# 道具
props = pygame.sprite.Group()

# 普通子弹
bullets = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    time_passed = clock.tick(60)
    time_passed_second = time_passed / 1000.
    current_time = pygame.time.get_ticks()

    c = randint(0, 100)
    if c == 1:
        A = hinder_classes.AmmunitionSupplyBox(screen)
        V1 = Vector2(randint(0, 800), randint(0, 458))
        A.put(V1)
        boxes.add(A)
    if c == 2:
        M = hinder_classes.MedicineSupplyBox(screen)
        V2 = Vector2(randint(0, 800), randint(0, 458))
        M.put(V2)
        boxes.add(M)

    pressed_mouse = pygame.mouse.get_pressed()
    if pressed_mouse[0]:
        mouse_pos = pygame.mouse.get_pos()
        bullet = bullet_classes.OrdinaryBullet(screen)
        bullet.fired(Vector2(mouse_pos[0], mouse_pos[1]), K_LEFT)
        bullets.add(bullet)

    for box in boxes.sprites():
        List = pygame.sprite.spritecollide(box, bullets, True)
        for r in List:
            if r:
                box.HP -= 2

    for b in boxes.sprites():
        if b.is_destroyed():
            p = b.open(current_time)
            b.kill()
            props.add(p)
    boxes.update()

    for b in bullets.sprites():
        if b.is_loss():
            b.kill()
    bullets.update(current_time, time_passed_second)

    for p in props.sprites():
        if p.is_loss(current_time):
            p.kill()
    props.update(current_time)

    screen.blit(background, (0, 0))

    boxes.draw(screen)
    props.draw(screen)
    bullets.draw(screen)

    pygame.display.update()
