import pygame
from pygame.locals import *
from gameobjects.vector2 import Vector2
import tank_classes
from random import randint


class TankGame:
    def __init__(self, player):
        self.player = player
        self.mix_AI = 10
        self.AI_tank_num_in_map = 0
        self.is_continue = True
        self.ordinary_tank_num = 20
        self.speed_tank_num = 10
        self.armoured_tank_num = 10
        self.is_game_over = False
        self.last_prop_car_time = 0
        self.prop_car_num = 0

    @classmethod
    def create_sprite_groups(cls):
        groups = {}
        # 创建一些游戏中的精灵组
        # 玩家坦克
        groups["player_tank"] = pygame.sprite.Group()
        # AI坦克
        groups["AI_tank"] = pygame.sprite.Group()
        # 道具车
        groups["prop_car"] = pygame.sprite.Group()
        # 道具箱
        groups["boxes"] = pygame.sprite.Group()
        # 普通子弹
        groups["ordinary_bullets"] = pygame.sprite.Group()
        # 特殊子弹
        groups["special_bullets"] = pygame.sprite.Group()
        # AI 子弹
        groups["ai_bullets"] = pygame.sprite.Group()
        # 道具
        groups["props"] = pygame.sprite.Group()
        # 爆炸
        groups["explode"] = pygame.sprite.Group()
        # 基地
        groups["base"] = pygame.sprite.Group()
        return groups

    @classmethod
    def keys_event_handle(cls, pressed_keys, p_tank, current_time, screen_pos, bullets, special_bullets):
        move = Vector2(0, 0)
        # 获取玩家坦克移动方向
        if pressed_keys[K_w]:
            move.y -= 1
            p_tank.change_direction(K_UP)
        elif pressed_keys[K_a]:
            move.x -= 1
            p_tank.change_direction(K_LEFT)
        elif pressed_keys[K_s]:
            move.y += 1
            p_tank.change_direction(K_DOWN)
        elif pressed_keys[K_d]:
            move.x += 1
            p_tank.change_direction(K_RIGHT)
        # 针对开火按键的处理
        if pressed_keys[K_h]:
            bullet = p_tank.fire(current_time, screen_pos)
            if bullet:
                bullets.add(bullet)
        elif pressed_keys[K_j]:
            s_bullet = p_tank.fire_a_fire(current_time, screen_pos)
            if s_bullet:
                special_bullets.add(s_bullet)
        elif pressed_keys[K_k]:
            s_bullet = p_tank.fire_a_electricity(current_time, screen_pos)
            if s_bullet:
                special_bullets.add(s_bullet)
        elif pressed_keys[K_l]:
            s_bullet = p_tank.fire_a_ice(current_time, screen_pos)
            if s_bullet:
                special_bullets.add(s_bullet)
        return move

    def collision_detection_handle(self, can_pass, can_not_pass, groups, base, map_borders, current_time):

        for box in groups["boxes"].sprites():
            # 盒子与玩家碰撞检测
            for tank in groups["player_tank"].sprites():
                if box.map_rect.colliderect(tank.map_rect):
                    tank.stop()
            # 盒子与AI
            for tank in groups["AI_tank"].sprites():
                if box.map_rect.colliderect(tank.map_rect):
                    tank.stop()
                    tank.strike()
            # 盒子与道具车
            for car in groups["prop_car"].sprites():
                if box.map_rect.colliderect(car.map_rect):
                    car.stop()
                    car.strike()
            # 盒子与玩家普通子弹的碰撞
            ob_list = pygame.sprite.spritecollide(box, groups["ordinary_bullets"], True)
            for r in ob_list:
                if r:
                    box.hurt(r.hurt_num)
            # 盒子与AI子弹碰撞
            pygame.sprite.spritecollide(box, groups["ai_bullets"], True)

        for pb in groups["ordinary_bullets"].sprites():
            # 玩家普通子弹与AI的碰撞
            for AI in groups["AI_tank"].sprites():
                if pb.map_rect.colliderect(AI.map_rect):
                    pb.kill()
                    AI.hurt(pb.hurt_num)
            # 玩家普通子弹与道具车的碰撞
            for car in groups["prop_car"].sprites():
                if pb.map_rect.colliderect(car.map_rect):
                    pb.kill()
                    car.hurt(pb.hurt_num)

        for sb in groups["special_bullets"].sprites():
            # 特殊子弹与AI碰撞
            for AI in groups["AI_tank"].sprites():
                if sb.map_rect.colliderect(AI.map_rect) and sb.is_new():
                    AI.hurt(sb.hurt_num)
                    sb.using()
                    print("OK")
                    if sb.attribute != "fire":
                        AI.get_state(sb.attribute, current_time)
            # 特殊子弹与道具车碰撞
            for AI in groups["prop_car"].sprites():
                if sb.map_rect.colliderect(AI.map_rect) and sb.is_new():
                    AI.hurt(sb.hurt_num)
                    sb.using()
                    print("OK")
                    if sb.attribute != "fire":
                        AI.get_state(sb.attribute, current_time)

        # AI子弹与玩家坦克的碰撞
        list_aib = pygame.sprite.spritecollide(groups["player_tank"].sprites()[0], groups["ai_bullets"], True)
        for aib in list_aib:
            if aib:
                groups["player_tank"].sprites()[0].hurt(aib.hurt_num, current_time)

        # AI与边界碰撞
        for AI in groups["AI_tank"].sprites():
            if AI.map_rect.collidelist(map_borders) != -1:
                AI.stop()
                AI.strike()

        # 道具车与边界碰撞
        for car in groups["prop_car"].sprites():
            if car.map_rect.collidelist(map_borders) != -1:
                car.stop()
                car.strike()

        # AI与地图障碍的碰撞
        for AI in groups["AI_tank"].sprites():
            if AI.map_rect.collidelist(can_pass) != -1:
                AI.stop()
                AI.strike()
            if AI.map_rect.collidelist(can_not_pass) != -1:
                AI.stop()
                AI.strike()

        # 道具车与地图障碍的碰撞
        for car in groups["prop_car"].sprites():
            if car.map_rect.collidelist(can_pass) != -1:
                car.stop()
                car.strike()
            if car.map_rect.collidelist(can_not_pass) != -1:
                car.stop()
                car.strike()

        # 玩家坦克与地图障碍的碰撞
        for tank in groups["player_tank"].sprites():
            if tank.map_rect.collidelist(can_pass) != -1:
                tank.stop()
            if tank.map_rect.collidelist(can_not_pass) != -1:
                tank.stop()

        # AI子弹与不可通过的地图障碍物碰撞
        for aib in groups["ai_bullets"].sprites():
            if aib.map_rect.collidelist(can_not_pass) != -1:
                aib.kill()

        # 玩家子弹与不可通过的地图障碍物碰撞
        for pb in groups["ordinary_bullets"].sprites():
            if pb.map_rect.collidelist(can_not_pass) != -1:
                pb.kill()

        # 玩家坦克与道具的碰撞
        for tank in groups["player_tank"].sprites():
            for prop in groups["props"].sprites():
                if tank.map_rect.colliderect(prop.map_rect):
                    if prop.prop_name == "electricity":
                        tank.electricity_num += 5
                    elif prop.prop_name == "fire":
                        tank.fire_num += 5
                    elif prop.prop_name == "ice":
                        tank.ice_num += 5
                    elif prop.prop_name == "HP":
                        tank.hp_up(4)
                    elif prop.prop_name == "life":
                        self.player.get_life()
                    elif prop.prop_name == "base_HP":
                        base.hp_up(8)
                    elif prop.prop_name == "coin":
                        self.player.mark_up(10)
                    else:
                        tank.get_speed_up(prop.prop_name, current_time)
                    prop.kill()

        # 基地与子弹
        for base in groups["base"].sprites():
            for ab in groups["ai_bullets"].sprites():
                if ab.map_rect.colliderect(base.map_rect):
                    base.hurt(ab.hurt_num)
                    ab.kill()
            for pb in groups["ordinary_bullets"].sprites():
                if pb.map_rect.colliderect(base.map_rect):
                    base.hurt(pb.hurt_num)
                    pb.kill()

        # 基地与玩家坦克和AI
        for base in groups["base"].sprites():
            for tank in groups["player_tank"].sprites():
                if tank.map_rect.colliderect(base.map_rect):
                    tank.stop()
            for AI in groups["AI_tank"].sprites():
                if AI.map_rect.colliderect(base.map_rect):
                    AI.stop()
                    AI.strike()
            for p_car in groups["prop_car"].sprites():
                if p_car.map_rect.colliderect(base.map_rect):
                    p_car.stop()
                    p_car.strike()

    def birth_ai_tank(self, screen, birth_poses, ai_tank, player_tank, prop_car, screen_pos, current_time, car_pos):
        pos_c = randint(0, 2)
        birth_pos = birth_poses[pos_c].copy()
        if (self.AI_tank_num_in_map < self.mix_AI) and (self.speed_tank_num > 0) and (self.ordinary_tank_num > 0) and (self.armoured_tank_num > 0):
            c = randint(0, 3)
            a = True
            while a:
                if c == 0 and self.speed_tank_num > 0:
                    tank = tank_classes.SpeedTank(screen)
                    tank.birth(birth_pos, player_tank, screen_pos)
                    ai_tank.add(tank)
                    self.speed_tank_num -= 1
                    a = False
                elif c == 1 and self.armoured_tank_num > 0:
                    tank = tank_classes.ArmouredTank(screen)
                    tank.birth(birth_pos, player_tank, screen_pos)
                    ai_tank.add(tank)
                    self.armoured_tank_num -= 1
                    a = False
                else:
                    tank = tank_classes.OrdinaryTank(screen)
                    tank.birth(birth_pos, player_tank, screen_pos)
                    ai_tank.add(tank)
                    self.ordinary_tank_num -= 1
                    a = False
            self.AI_tank_num_in_map += 1
        if (self.last_prop_car_time + 10000 < current_time) and (self.prop_car_num < 3):
            print(self.last_prop_car_time, current_time)
            car = tank_classes.PropCar(screen)
            car.birth(car_pos.copy(), player_tank, screen_pos)
            print(car.map_pos, car.position)
            prop_car.add(car)
            self.prop_car_num += 1

            self.last_prop_car_time = current_time

    def death_detection_handle(self, screen, groups, current_time, time_passed_second, screen_pos, player_birth_pos, move):
        # 玩家子弹死亡检测
        for b in groups["ordinary_bullets"].sprites():
            if b.is_loss():
                b.kill()
        groups["ordinary_bullets"].update(current_time, time_passed_second, screen_pos)

        # 特殊子弹死亡检测
        for sb in groups["special_bullets"].sprites():
            if sb.is_loss():
                sb.kill()
        groups["special_bullets"].update(current_time, screen_pos)

        # AI子弹死亡检测
        for ab in groups["ai_bullets"].sprites():
            if ab.is_loss():
                ab.kill()
        groups["ai_bullets"].update(current_time, time_passed_second, screen_pos)

        # 盒子死亡检测
        for b in groups["boxes"].sprites():
            if b.is_destroyed():
                prop = b.open(current_time)
                b.kill()
                groups["props"].add(prop)
        groups["boxes"].update(screen_pos)

        # 玩家死亡检测
        for tank in groups["player_tank"].sprites():
            if tank.is_dead():
                tank.kill()
                p_tank = self.player.birth_a_tank(screen, Vector2(400, 240), current_time, player_birth_pos["player"])
                groups["player_tank"].add(p_tank)
        groups["player_tank"].update(current_time, time_passed_second, move, screen_pos)

        # AI死亡检测
        for AI in groups["AI_tank"]:
            if AI.is_dead():
                e = AI.explode(screen_pos)
                if e:
                    groups["explode"].add(e)
                AI.kill()
                self.AI_tank_num_in_map -= 1
        groups["AI_tank"].update(current_time, time_passed_second, screen_pos)

        # 道具车死亡检测
        for p_car in groups["prop_car"].sprites():
            if p_car.is_dead():
                e = p_car.explode(screen_pos)
                if e:
                    groups["explode"].add(e)
                pr = p_car.open(current_time, screen_pos)
                p_car.kill()
                self.prop_car_num -= 1
                groups["props"].add(pr)
        groups["prop_car"].update(current_time, time_passed_second, screen_pos)

        # 基地死亡检测
        for base in groups["base"].sprites():
            if base.is_destroyed():
                e = base.explode()
                groups["explode"].add(e)
                b.kill()
                self.is_game_over = True
        groups["base"].update(screen_pos)

        # 道具死亡检测
        for p in groups["props"].sprites():
            if p.is_loss(current_time):
                p.kill()
        groups["props"].update(current_time, screen_pos)

        # 爆炸死亡检测
        for e in groups["explode"].sprites():
            if e.is_loss():
                e.kill()
        groups["explode"].update(current_time, screen_pos)

    def state_detection_handle(self, groups, current_time):

        # AI状态检测
        # 接收AI发射的子弹，以及状态检测测
        for AI in groups["AI_tank"].sprites():
            AI.get_rid_of_state(current_time)
            ab = AI.ai_fire()
            if ab:
                groups["ai_bullets"].add(ab)

        # 玩家坦克状态检测
        self.player.tank.prop_time_out(current_time)
