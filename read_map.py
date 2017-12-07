from pytmx.util_pygame import load_pygame
from pygame.locals import Rect
from gameobjects.vector2 import Vector2


# 固定地图算法实现
def read_map(map_name, map_surface):
    """
    :param map_name: tmx 的路径名称
    :param map_surface: 将tile绘制到的目标 Surface 对象
    :return: void
    """
    tiled_map = load_pygame(map_name)
    for y in range(tiled_map.height):
        for x in range(tiled_map.width):
            screen_x = x * tiled_map.tilewidth
            screen_y = y * tiled_map.tileheight
            pygame_surface = tiled_map.get_tile_image(x, y, 1)
            if pygame_surface:
                map_surface.blit(pygame_surface, (screen_x, screen_y))


# 多层地图算法实现
def read_map_multi(map_name, map_surface, layers_nums):
    """
    :param map_name: tmx 的路径名称
    :param map_surface: 将tile绘制到的目标 Surface 对象
    :param layers_nums: 所导入的 tmx 文件中图形层的个数
    :return: void
    """
    tiled_map = load_pygame(map_name)
    for layer in range(layers_nums):
        for y in range(tiled_map.height):
            for x in range(tiled_map.width):
                screen_x = x * tiled_map.tilewidth
                screen_y = y * tiled_map.tileheight
                pygame_surface = tiled_map.get_tile_image(x, y, layer)
                if pygame_surface:
                    map_surface.blit(pygame_surface, (screen_x, screen_y))


# 滚动地图算法实现
def read_map_roll(map_name, map_surface, layers_nums, pos, screen_size):
    """
    :param map_name: tmx 的路径名称
    :param map_surface: 将tile绘制到的目标 Surface 对象
    :param layers_nums: 所导入的 tmx 文件中图形层的个数
    :param pos: 玩家坦克相对于地图的所在位置，为二维向量
    :param screen_size: 实际屏幕的大小，为元组
    :return: void
    """
    tiled_map = load_pygame(map_name)
    player_pos = pos.copy()
    if player_pos.x < screen_size[0] / 2:
        player_pos.x = screen_size[0] / 2
    if player_pos.x > tiled_map.width * tiled_map.tilewidth - screen_size[0] / 2:
        player_pos.x = tiled_map.width * tiled_map.tilewidth - screen_size[0] / 2
    if player_pos.y < screen_size[1] / 2:
        player_pos.y = screen_size[1] / 2
    if player_pos.y > tiled_map.height * tiled_map.tileheight - screen_size[1] / 2:
        player_pos.y = tiled_map.height * tiled_map.tileheight - screen_size[1] / 2
    tile_player_x = int(player_pos.x // tiled_map.tilewidth)
    tile_player_y = int(player_pos.y // tiled_map.tileheight)
    begin_x = tile_player_x - 5
    begin_y = tile_player_y - 5
    if begin_x < 0:
        begin_x = 0

    if begin_x > 10:
        begin_x = 10

    if begin_y < 0:
        begin_y = 0

    if begin_y > 10:
        begin_y = 10

    end_x = begin_x + 10
    end_y = begin_y + 10

    for layer in range(layers_nums):
        for y in range(begin_y, end_y):
            for x in range(begin_x, end_x):

                screen_x = x * tiled_map.tilewidth - player_pos.x + screen_size[0] / 2
                screen_y = y * tiled_map.tileheight - player_pos.y + screen_size[1] / 2
                pygame_surface = tiled_map.get_tile_image(x, y, layer)
                if pygame_surface:
                    map_surface.blit(pygame_surface, (screen_x, screen_y))

    return Vector2(player_pos.x - screen_size[0] / 2, player_pos.y - screen_size[1] / 2)


# 绘制滚动地图中的某一层
def draw_a_layer_in_roll(map_name, map_surface, layer_num, pos, screen_size):
    """
    :param map_name: tmx 的路径名称
    :param map_surface: 将tile绘制到的目标 Surface 对象
    :param layer_num: 所需要单独绘制的图形层的序号
    :param pos: 玩家坦克相对于地图的所在位置，为二维向量
    :param screen_size: 实际屏幕的大小，为元组
    :return: void
    """
    tiled_map = load_pygame(map_name)
    player_pos = pos.copy()
    if player_pos.x < screen_size[0] / 2:
        player_pos.x = screen_size[0] / 2
    if player_pos.x > tiled_map.width * tiled_map.tilewidth - screen_size[0] / 2:
        player_pos.x = tiled_map.width * tiled_map.tilewidth - screen_size[0] / 2
    if player_pos.y < screen_size[1] / 2:
        player_pos.y = screen_size[1] / 2
    if player_pos.y > tiled_map.height * tiled_map.tileheight - screen_size[1] / 2:
        player_pos.y = tiled_map.height * tiled_map.tileheight - screen_size[1] / 2
    tile_player_x = int(player_pos.x // tiled_map.tilewidth)
    tile_player_y = int(player_pos.y // tiled_map.tileheight)
    begin_x = tile_player_x - 5
    begin_y = tile_player_y - 5
    if begin_x < 0:
        begin_x = 0

    if begin_x > 10:
        begin_x = 10

    if begin_y < 0:
        begin_y = 0

    if begin_y > 10:
        begin_y = 10

    end_x = begin_x + 10
    end_y = begin_y + 10

    for y in range(begin_y, end_y):
        for x in range(begin_x, end_x):

            screen_x = x * tiled_map.tilewidth - player_pos.x + screen_size[0] / 2
            screen_y = y * tiled_map.tileheight - player_pos.y + screen_size[1] / 2
            pygame_surface = tiled_map.get_tile_image(x, y, layer_num)
            if pygame_surface:
                map_surface.blit(pygame_surface, (screen_x, screen_y))


# 从制定的对象层取出所有对象的矩形框
def get_object(map_name, object_layer_name):
    """
    :param map_name: tmx 的路径名称
    :param object_layer_name: 对象层的名称
    :return: 元素为矩形的列表
    """
    tiled_map = load_pygame(map_name)
    object_layer = tiled_map.get_layer_by_name(object_layer_name)
    objects = []
    for a_object in object_layer:
        objects.append(Rect(a_object.x, a_object.y, a_object.width, a_object.height))
    return objects
