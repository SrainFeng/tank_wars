import pygame
from pygame.locals import *
from gameobjects.vector2 import Vector2
import bullet_classes, base_class

pygame.init()
screen = pygame.display.set_mode((800, 458), 0, 32)
pygame.display.set_caption("碰撞测试")

background = pygame.image.load("84.jpg").convert_alpha()

clock = pygame.time.Clock()

# 创建一些精灵组
# 爆炸
explodes = pygame.sprite.Group()

# 基地
bases = pygame.sprite.Group()

# 普通子弹
bullets = pygame.sprite.Group()

B = base_class.Base(screen)
V1 = Vector2(400, 400)
B.put(V1)
bases.add(B)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    time_passed = clock.tick(60)
    time_passed_second = time_passed / 1000.
    current_time = pygame.time.get_ticks()

    pressed_mouse = pygame.mouse.get_pressed()
    if pressed_mouse[0]:
        mouse_pos = pygame.mouse.get_pos()
        bullet = bullet_classes.OrdinaryBullet(screen)
        bullet.fired(Vector2(mouse_pos[0], mouse_pos[1]))
        bullets.add(bullet)

    for base in bases.sprites():
        List = pygame.sprite.spritecollide(base, bullets, True)
        for r in List:
            if r:
                base.HP -= 2

    for b in bases.sprites():
        if b.is_destroyed():
            e = b.explode()
            print(e)
            explodes.add(e)
            b.kill()
    bases.update()

    for ex in explodes.sprites():
        if ex.is_loss():
            explodes.remove(ex)
            
    explodes.update(current_time)

    for b in bullets.sprites():
        if b.is_loss():
            b.kill()
    bullets.update(current_time, time_passed_second, "down")

    screen.blit(background, (0, 0))

    bases.draw(screen)
    bullets.draw(screen)
    explodes.draw(screen)

    pygame.display.update()
