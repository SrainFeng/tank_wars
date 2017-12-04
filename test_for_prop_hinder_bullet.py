import pygame
from pygame.locals import *
from gameobjects.vector2 import Vector2
import hinder_classes
from random import randint
from tank_classes import PlayerTank

pygame.init()
screen = pygame.display.set_mode((800, 458), 0, 32)
pygame.display.set_caption("碰撞测试")

background = pygame.image.load("84.jpg").convert_alpha()

clock = pygame.time.Clock()

# 创建一些精灵组
# 玩家坦克
current_time = pygame.time.get_ticks()
player_tank = pygame.sprite.Group()
tank = PlayerTank(screen)
tank.birth(Vector2(100, 100), current_time)
player_tank.add(tank)

# 道具箱
boxes = pygame.sprite.Group()

# 道具
props = pygame.sprite.Group()

# 普通子弹
bullets = pygame.sprite.Group()

while True:
    time_passed = clock.tick(60)
    time_passed_second = time_passed / 1000.
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    pressed_keys = pygame.key.get_pressed()

    move = Vector2(0, 0)
    if pressed_keys[K_LEFT]:
        move.x -= 1
        tank.change_direction(K_LEFT)
    if pressed_keys[K_RIGHT]:
        move.x += 1
        tank.change_direction(K_RIGHT)
    if pressed_keys[K_UP]:
        move.y -= 1
        tank.change_direction(K_UP)
    if pressed_keys[K_DOWN]:
        move.y += 1
        tank.change_direction(K_DOWN)

    if pressed_keys[K_SPACE]:
        bullet = tank.fire(current_time)
        if bullet:
            bullets.add(bullet)

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

    for box in boxes.sprites():
        List = pygame.sprite.spritecollide(box, bullets, True)
        for r in List:
            if r:
                box.HP -= 2

    ListB = pygame.sprite.spritecollide(tank, boxes, False)
    if ListB:
        tank.stop()

    player_tank.update(current_time, time_passed_second, move)

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

    for i in bullets.sprites():
        print(i.image)

    for p in props.sprites():
        if p.is_loss(current_time):
            p.kill()
    props.update(current_time)

    screen.blit(background, (0, 0))

    boxes.draw(screen)
    props.draw(screen)
    player_tank.draw(screen)
    bullets.draw(screen)

    pygame.display.update()
