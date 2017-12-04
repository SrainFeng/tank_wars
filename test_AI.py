import pygame
from pygame.locals import *
from gameobjects.vector2 import Vector2
import hinder_classes
from random import randint
import tank_classes


screen_top = Rect(0, -1, 800, 1)
screen_bottom = Rect(0, 458, 800, 1)
screen_left = Rect(-1, 0, 1, 458)
screen_right = Rect(800, 0, 1, 458)
screen_borders = [screen_bottom, screen_left, screen_right, screen_top]

pygame.init()
screen = pygame.display.set_mode((800, 458), 0, 32)
pygame.display.set_caption("碰撞测试")

background = pygame.image.load("84.jpg").convert_alpha()

clock = pygame.time.Clock()

# 创建一些精灵组
# 玩家坦克
current_time = pygame.time.get_ticks()
player_tank = pygame.sprite.Group()
tank1 = tank_classes.PlayerTank(screen)
tank1.birth(Vector2(700, 100), current_time)
player_tank.add(tank1)

# AI坦克
AI_tank = pygame.sprite.Group()
tank2 = tank_classes.PropCar(screen)
tank2.birth(Vector2(400, 200), player_tank)
AI_tank.add(tank2)

# 道具箱
boxes = pygame.sprite.Group()

for i in range(5):
    c = randint(1, 2)
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

# 道具
props = pygame.sprite.Group()

# 普通子弹
bullets = pygame.sprite.Group()

# AI 子弹
ai_bullets = pygame.sprite.Group()

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
        tank1.change_direction(K_LEFT)
    if pressed_keys[K_RIGHT]:
        move.x += 1
        tank1.change_direction(K_RIGHT)
    if pressed_keys[K_UP]:
        move.y -= 1
        tank1.change_direction(K_UP)
    if pressed_keys[K_DOWN]:
        move.y += 1
        tank1.change_direction(K_DOWN)

    if pressed_keys[K_SPACE]:
        bullet = tank1.fire(current_time)
        if bullet:
            bullets.add(bullet)

    # 盒子与玩家子弹的碰撞
    for box in boxes.sprites():
        List = pygame.sprite.spritecollide(box, bullets, True)
        for r in List:
            if r:
                box.HP -= 2

    # 盒子与AI子弹 碰撞
    for box in boxes.sprites():
        List = pygame.sprite.spritecollide(box, ai_bullets, True)

    # AI子弹与玩家坦克的碰撞
    List_aib = pygame.sprite.spritecollide(tank1, ai_bullets, True)
    for aib in List_aib:
        if aib:
            tank1.hurt(aib.hurt_num, current_time)

    # 玩家子弹与AI的碰撞
    List_pb = pygame.sprite.spritecollide(tank2, bullets, True)
    for pb in List_pb:
        if pb:
            tank2.hurt(pb.hurt_num)

    # 盒子与玩家
    ListB = pygame.sprite.spritecollide(tank1, boxes, False)
    if ListB:
        tank1.stop()

    # 盒子与AI
    ListA = pygame.sprite.spritecollide(tank2, boxes, False)
    if ListA:
        tank2.stop()
        tank2.strike()

    # AI与边界碰撞
    if tank2.rect.collidelist(screen_borders) != -1:
        tank2.stop()
        tank2.strike()

    player_tank.update(current_time, time_passed_second, move)

    # 接收AI发射的子弹
    ab = tank2.ai_fire()
    if ab:
        ai_bullets.add(ab)

    # 玩家死亡检测
    if tank1.is_dead():
        break

    # AI死亡检测
    if tank2.is_dead():
        tank2.kill()
        tank2 = tank_classes.PropCar(screen)
        tank2.birth(Vector2(700, 400), player_tank)
        AI_tank.add(tank2)

    AI_tank.update(current_time, time_passed_second)

    # 盒子死亡检测
    for b in boxes.sprites():
        if b.is_destroyed():
            p = b.open(current_time)
            b.kill()
            props.add(p)
    boxes.update()

    # 玩家子弹死亡检测
    for b in bullets.sprites():
        if b.is_loss():
            b.kill()
    bullets.update(current_time, time_passed_second)

    # AI子弹死亡检测
    for ab in ai_bullets.sprites():
        if ab.is_loss():
            ab.kill()
    ai_bullets.update(current_time, time_passed_second)

    # 道具死亡检测
    for p in props.sprites():
        if p.is_loss(current_time):
            p.kill()
    props.update(current_time)

    screen.blit(background, (0, 0))

    boxes.draw(screen)
    props.draw(screen)
    player_tank.draw(screen)
    AI_tank.draw(screen)
    bullets.draw(screen)
    ai_bullets.draw(screen)

    pygame.display.update()
