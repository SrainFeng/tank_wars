import pygame
from pygame.locals import *
import read_map
import tank_classes
from gameobjects.vector2 import Vector2
from random import randint
import hinder_classes

map_top = Rect(0, -1, 1600, 1)
map_bottom = Rect(0, 1600, 1600, 1)
map_left = Rect(-1, 0, 1, 1600)
map_right = Rect(1600, 0, 1, 1600)
map_borders = [map_bottom, map_left, map_right, map_top]

pygame.init()

screen = pygame.display.set_mode((800, 480), 0, 32)

map_surface = pygame.Surface((832, 512), 0, 32)

clock = pygame.time.Clock()

# 创建一些精灵组
# 玩家坦克
current_time = pygame.time.get_ticks()
player_tank = pygame.sprite.Group()
tank1 = tank_classes.PlayerTank(screen)
tank1.birth(Vector2(400, 240), current_time, Vector2(1200, 1200))
player_tank.add(tank1)

# AI坦克
AI_tank = pygame.sprite.Group()
tank2 = tank_classes.PropCar(screen)
tank2.birth(Vector2(400, 200), player_tank, Vector2(800, 960))
AI_tank.add(tank2)

# 道具箱
boxes = pygame.sprite.Group()

# 普通子弹
bullets = pygame.sprite.Group()

# AI 子弹
ai_bullets = pygame.sprite.Group()

# 道具
props = pygame.sprite.Group()

# 特殊子弹
special_bullets = pygame.sprite.Group()

# 爆炸
explode = pygame.sprite.Group()


while True:
    time_passed = clock.tick(60)
    time_passed_second = time_passed / 1000.
    current_time = pygame.time.get_ticks()
    screen_pos = read_map.read_map_roll("map/map1.tmx", map_surface, 3, tank1.map_pos, (800, 480))
    print(tank2.map_pos)

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    pressed_keys = pygame.key.get_pressed()

    move = Vector2(0, 0)
    if pressed_keys[K_w]:
        move.y -= 1
        tank1.change_direction(K_UP)
    elif pressed_keys[K_a]:
        move.x -= 1
        tank1.change_direction(K_LEFT)
    elif pressed_keys[K_s]:
        move.y += 1
        tank1.change_direction(K_DOWN)
    elif pressed_keys[K_d]:
        move.x += 1
        tank1.change_direction(K_RIGHT)
    if pressed_keys[K_SPACE]:
        bullet = tank1.fire(current_time, screen_pos)
        if bullet:
            bullets.add(bullet)
    elif pressed_keys[K_b]:
        s_bullet = tank1.fire_a_fire(current_time, screen_pos)
        if s_bullet:
            special_bullets.add(s_bullet)
    elif pressed_keys[K_n]:
        s_bullet = tank1.fire_a_electricity(current_time, screen_pos)
        if s_bullet:
            special_bullets.add(s_bullet)
    elif pressed_keys[K_m]:
        s_bullet = tank1.fire_a_ice(current_time, screen_pos)
        if s_bullet:
            special_bullets.add(s_bullet)

    # 碰撞检测
    # 盒子与玩家碰撞检测
    for box in boxes.sprites():
        if box.map_rect.colliderect(tank1.map_rect):
            tank1.stop()
    player_tank.update(current_time, time_passed_second, move, screen_pos)

    # 盒子与AI
    for box in boxes.sprites():
        if box.map_rect.colliderect(tank2.map_rect):
            tank2.stop()
            tank2.strike()

    # 盒子与玩家子弹的碰撞
    for box in boxes.sprites():
        List = pygame.sprite.spritecollide(box, bullets, True)
        for r in List:
            if r:
                box.hurt(r.hurt_num)

    # 盒子与AI子弹 碰撞
    for box in boxes.sprites():
        List = pygame.sprite.spritecollide(box, ai_bullets, True)

    # 玩家子弹与AI的碰撞
    for pb in bullets.sprites():
        for AI in AI_tank.sprites():
            if pb.map_rect.colliderect(AI.map_rect):
                pb.kill()
                AI.hurt(pb.hurt_num)

    # 特殊子弹与AI碰撞
    for sb in special_bullets.sprites():
        for AI in AI_tank.sprites():
            if sb.map_rect.colliderect(AI.map_rect) and sb.is_new():
                AI.hurt(sb.hurt_num)
                sb.using()
                print("OK")
                if sb.attribute != "fire":
                    AI.get_state(sb.attribute, current_time)

    # AI子弹与玩家坦克的碰撞
    List_aib = pygame.sprite.spritecollide(tank1, ai_bullets, True)
    for aib in List_aib:
        if aib:
            tank1.hurt(aib.hurt_num, current_time)

    # 接收AI发射的子弹
    ab = tank2.ai_fire()
    if ab:
        ai_bullets.add(ab)

    # AI与边界碰撞
    if tank2.map_rect.collidelist(map_borders) != -1:
        tank2.stop()
        tank2.strike()

    # AI状态检测
    for AI in AI_tank.sprites():
        AI.get_rid_of_state(current_time)

    # 死亡检测
    # 玩家子弹死亡检测
    for b in bullets.sprites():
        if b.is_loss():
            b.kill()
    bullets.update(current_time, time_passed_second, screen_pos)

    # 特殊子弹死亡检测
    for sb in special_bullets.sprites():
        if sb.is_loss():
            sb.kill()
    special_bullets.update(current_time, screen_pos)

    # AI子弹死亡检测
    for ab in ai_bullets.sprites():
        if ab.is_loss():
            ab.kill()
    ai_bullets.update(current_time, time_passed_second, screen_pos)

    # 盒子死亡检测
    for b in boxes.sprites():
        if b.is_destroyed():
            p = b.open(current_time)
            b.kill()
            props.add(p)
    boxes.update(screen_pos)

    # 玩家死亡检测
    if tank1.is_dead():
        break

    # AI死亡检测
    for AI in AI_tank:
        if AI.is_dead():
            e = AI.explode(screen_pos)
            if e:
                explode.add(e)
            pr = tank2.open(current_time, screen_pos)
            print(pr)
            AI.kill()
            props.add(pr)
            tank2 = tank_classes.PropCar(screen)
            tank2.birth(Vector2(400, 200), player_tank, screen_pos)
            AI_tank.add(tank2)
    AI_tank.update(current_time, time_passed_second, screen_pos)

    # 道具死亡检测
    for p in props.sprites():
        if p.is_loss(current_time):
            p.kill()
    props.update(current_time, screen_pos)

    # 爆炸死亡检测
    for e in explode.sprites():
        if e.is_loss():
            e.kill()
    explode.update(current_time, screen_pos)

    # 屏幕绘制
    screen.blit(map_surface, (0, 0))
    props.draw(screen)
    player_tank.draw(screen)
    boxes.draw(screen)
    bullets.draw(screen)
    ai_bullets.draw(screen)
    AI_tank.draw(screen)
    special_bullets.draw(screen)
    explode.draw(screen)

    c = randint(0, 100)
    if c == 1:
        A = hinder_classes.AmmunitionSupplyBox(screen)
        V1 = Vector2(randint(0, 1600), randint(0, 1600))
        A.put(V1, screen_pos)
        boxes.add(A)
    if c == 2:
        M = hinder_classes.MedicineSupplyBox(screen)
        V2 = Vector2(randint(0, 1600), randint(0, 1600))
        M.put(V2, screen_pos)
        boxes.add(M)

    pygame.display.update()
