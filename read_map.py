from pytmx.util_pygame import load_pygame


# 多层地图算法实现
def read_map(map_name, map_surface, layers_nums):
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
    tileplayerx = int(player_pos.x // tiled_map.tilewidth)
    tileplayery = int(player_pos.y // tiled_map.tileheight)
    begainx = tileplayerx - 5
    begainy = tileplayery - 5
    if begainx < 0:
        begainx = 0

    if begainx > 10:
        begainx = 10

    if begainy < 0:
        begainy = 0

    if begainy > 10:
        begainy = 10

    endx = begainx + 10
    endy = begainy + 10

    for layer in range(layers_nums):
        for y in range(begainy, endy):
            for x in range(begainx, endx):

                screen_x = x * tiled_map.tilewidth - player_pos.x + screen_size[0] / 2
                screen_y = y * tiled_map.tileheight - player_pos.y + screen_size[1] / 2
                pygame_surface = tiled_map.get_tile_image(x, y, layer)
                if pygame_surface:
                    map_surface.blit(pygame_surface, (screen_x, screen_y))
