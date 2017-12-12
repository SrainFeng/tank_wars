import pygame
from pygame.locals import *
import game
import read_map
import player_class
from gameobjects.vector2 import Vector2
import base_class
import hinder_classes
from random import randint

# 主界面图片路径
menu_background = "source_material/main_menu/background.png"
menu_button = "source_material/main_menu/button.png"
map1 = "map/map1.tmx"

# 游戏界面UI
electricity_num_name = "source_material/UI/electricity_num.png"
fire_num_name = "source_material/UI/fire_num.png"
ice_num_name = "source_material/UI/ice_num.png"
life_UI_name = "source_material/UI/life.png"
a_tank_name = "source_material/UI/a_tk.png"
s_tank_name = "source_material/UI/s_tk.png"
o_tank_name = "source_material/UI/o_tk.png"

# 初始化 pygame 的一些内置数据
pygame.init()
# 创建一个窗口，大小 800 * 480
screen = pygame.display.set_mode((800, 480), 0, 32)
# 初始化一个计时器
clock = pygame.time.Clock()
# 创建主界面 Surface 对象
background = pygame.image.load(menu_background).convert()
button = pygame.image.load(menu_button).convert_alpha()
background.blit(button, (330, 400))

# 主窗口循环
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    # 获取鼠标的位置和点击的情况
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # 游戏循环，点击在按钮图片位置时进入游戏
    if mouse_pressed[0] and (330 < mouse_pos[0] < 470) and (400 < mouse_pos[1] < 424):
        # 创建一些游戏中的精灵组,存在一个字典中
        groups = game.TankGame.create_sprite_groups()
        # 用于绘制滚动地图的 Surface 对象
        map_surface = pygame.Surface((832, 512), 0, 32)
        font = pygame.font.Font("李旭科书法1.4.ttf", 40)
        electricity_num = pygame.image.load(electricity_num_name).convert_alpha()
        fire_num = pygame.image.load(fire_num_name).convert_alpha()
        ice_num = pygame.image.load(ice_num_name).convert_alpha()
        life_num = pygame.image.load(life_UI_name).convert_alpha()
        a_tank = pygame.image.load(a_tank_name).convert_alpha()
        s_tank = pygame.image.load(s_tank_name).convert_alpha()
        o_tank = pygame.image.load(o_tank_name).convert_alpha()

        # 读取地图中的对象层
        # 基地与玩家
        player_birth_pos = read_map.get_objects_position_for_base(map1, "base")
        # 道具箱位置
        boxes_pos = read_map.get_objects_position(map1, "prop_boxes")
        # 子弹可以透过的碰撞区域
        can_pass = read_map.get_objects(map1, "bullet_can_pass")
        # 子弹不可透过的碰撞区域
        can_not_pass = read_map.get_objects(map1, "bullet_can_not_pass")
        # AI 坦克出生位置
        AI_birth_pos = read_map.get_objects_position(map1, "AI_birth")
        # 道具车出生位置
        prop_car_birth_pos = read_map.get_objects_position(map1, "prop_car")

        map_top = Rect(0, -1, 1600, 1)
        map_bottom = Rect(0, 1600, 1600, 1)
        map_left = Rect(-1, 0, 1, 1600)
        map_right = Rect(1600, 0, 1, 1600)
        map_borders = [map_bottom, map_left, map_right, map_top]

        # print(player_birth_pos)
        # print(boxes_pos)
        # print(can_pass)
        # print(can_not_pass)
        # print(AI_birth_pos)
        # print(prop_car_birth_pos)

        # 获取当前时间
        current_time = pygame.time.get_ticks()
        # 创建一个新的玩家对象
        new_player = player_class.Player()
        # 生成玩家坦克
        p_tank = new_player.birth_a_tank(screen, Vector2(400, 240), current_time, player_birth_pos["player"].copy())
        # 将玩家坦克加入玩家坦克的精灵组中
        groups["player_tank"].add(p_tank)

        # 创建基地
        screen_start_pos = Vector2(441, 1096)
        base = base_class.Base(screen)
        base.put(player_birth_pos["base"], screen_start_pos)
        groups["base"].add(base)

        # 生成道具箱
        for pos in boxes_pos:
            c = randint(0, 1)
            if c == 0:
                A = hinder_classes.AmmunitionSupplyBox(screen)
                A.put(pos, screen_start_pos)
                groups["boxes"].add(A)
            elif c == 1:
                M = hinder_classes.MedicineSupplyBox(screen)
                M.put(pos, screen_start_pos)
                groups["boxes"].add(M)

        # 创建一个游戏对象
        new_game = game.TankGame(new_player)
        while True:
            # 使用计时器设置帧率
            time_passed = clock.tick(60)
            # 获取每两次循环的间隔时间并转换单位为秒
            time_passed_second = time_passed / 1000.
            # 获取当前时间
            current_time = pygame.time.get_ticks()
            # 读取并绘制滚动地图，获取当前屏幕相对于整个地图的位置
            screen_pos = read_map.read_map_roll(map1, map_surface, 3, new_game.player.tank.map_pos, (800, 480))
            # 处理用户输入
            # 处理退出事件
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            # 获取键盘的按键按下的状况
            pressed_keys = pygame.key.get_pressed()
            # 键盘输入的处理
            move = game.TankGame.keys_event_handle(pressed_keys, new_player.tank, current_time, screen_pos, groups["ordinary_bullets"], groups["special_bullets"])

            # 一系列的碰撞检测处理
            new_game.collision_detection_handle(can_pass, can_not_pass, groups, base, map_borders, current_time)

            # 生成AI坦克
            new_game.birth_ai_tank(screen, AI_birth_pos, groups["AI_tank"], groups["player_tank"], groups["prop_car"], screen_pos, current_time, prop_car_birth_pos[0])

            # 状态检测
            new_game.state_detection_handle(groups, current_time)

            # 精灵死亡检测
            new_game.death_detection_handle(screen, groups, current_time, time_passed_second, screen_pos, player_birth_pos.copy(), move)

            # 地图绘制
            screen.blit(map_surface, (0, 0))

            # 绘制所有精灵
            for value in groups.values():
                value.draw(screen)

            life_text_surface = font.render(str(new_game.player.life), True, (0, 0, 0))
            fire_text_surface = font.render(str(new_game.player.tank.fire_num), True, (0, 0, 0))
            electricity_text_surface = font.render(str(new_game.player.tank.electricity_num), True, (0, 0, 0))
            ice_text_surface = font.render(str(new_game.player.tank.ice_num), True, (0, 0, 0))
            o_tank_text_surface = font.render(str(new_game.last_o_tk), True, (0, 0, 0))
            s_tank_text_surface = font.render(str(new_game.last_s_tk), True, (0, 0, 0))
            a_tank_text_surface = font.render(str(new_game.last_a_tk), True, (0, 0, 0))

            # 玩家状态
            screen.blit(life_num, (10, 10))
            screen.blit(life_text_surface, (50, 10))
            screen.blit(fire_num, (10, 50))
            screen.blit(fire_text_surface, (50, 50))
            screen.blit(electricity_num, (10, 90))
            screen.blit(electricity_text_surface, (50, 90))
            screen.blit(ice_num, (10, 130))
            screen.blit(ice_text_surface, (50, 130))
            # 绘制玩家血条
            HP_bar_health = Rect(90, 30, new_game.player.tank.HP / 10 * 100, 10)
            HP_bar = Rect(90, 30, 100, 10)
            pygame.draw.rect(screen, (255, 0, 0), HP_bar)
            pygame.draw.rect(screen, (0, 255, 0), HP_bar_health)
            # 剩余敌人数量
            screen.blit(o_tank, (700, 10))
            screen.blit(o_tank_text_surface, (740, 10))
            screen.blit(s_tank, (700, 50))
            screen.blit(s_tank_text_surface, (740, 50))
            screen.blit(a_tank, (700, 90))
            screen.blit(a_tank_text_surface, (740, 90))

            '''groups["player_tank"].draw(screen)
            # AI坦克
            groups["AI_tank"].draw(screen)
            # 道具车
            groups["prop_car"].draw(screen)
            # 道具箱
            groups["boxes"].draw(screen)
            # 普通子弹
            groups["ordinary_bullets"].draw(screen)
            # 特殊子弹
            groups["special_bullets"].draw(screen)
            # AI 子弹
            groups["ai_bullets"].draw(screen)
            # 道具
            groups["props"].draw(screen)
            # 爆炸
            groups["explode"].draw(screen)
            # 基地
            groups["base"].draw(screen)'''

            pygame.display.update()

            if new_game.is_game_over:
                break

            '''print(len(groups["AI_tank"]))
            print("tank HP:" + str(new_game.player.tank.HP))
            print("life:" + str(new_game.player.life))'''

    # 将背景绘制到屏幕上
    screen.blit(background, (0, 0))
    # 更新重绘
    pygame.display.update()

