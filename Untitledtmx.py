import pygame
from pygame.locals import *
import read_map
import tank_classes
from gameobjects.vector2 import Vector2

pygame.init()

screen = pygame.display.set_mode((224, 224), 0, 32)

map_surface = pygame.Surface((256, 256), 0, 32)

clock = pygame.time.Clock()

# 获取地图中的某一层的对象，返回对象矩形列表
objects = read_map.get_object("map/tmxtry.tmx", "object")

print(objects)

# 创建一些精灵组
# 玩家坦克
current_time = pygame.time.get_ticks()
player_tank = pygame.sprite.Group()
tank1 = tank_classes.PlayerTank(screen)
tank1.birth(Vector2(112, 112), current_time, Vector2(320, 320))
player_tank.add(tank1)


# print(len(tiled_map.layers))

# for layer in tiled_map.layers:
#   print(type(layer))

while True:
    time_passed = clock.tick(60)
    time_passed_second = time_passed / 1000.
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    pressed_keys = pygame.key.get_pressed()

    move = Vector2(0, 0)
    if pressed_keys[K_UP]:
        move.y -= 1
        tank1.change_direction(K_UP)
    elif pressed_keys[K_LEFT]:
        move.x -= 1
        tank1.change_direction(K_LEFT)
    elif pressed_keys[K_DOWN]:
        move.y += 1
        tank1.change_direction(K_DOWN)
    elif pressed_keys[K_RIGHT]:
        move.x += 1
        tank1.change_direction(K_RIGHT)

    read_map.read_map_roll("map/tmxtry.tmx", map_surface, 2, tank1.map_pos, (224, 224))
    screen.blit(map_surface, (0, 0))
    player_tank.update(current_time, time_passed_second, move)
    player_tank.draw(screen)

    # screen.blit(pygame_surface, (0, 0))
    pygame.display.update()


