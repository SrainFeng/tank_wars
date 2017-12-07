import tank_sprite
import state_machine
from pygame.locals import *
from gameobjects.vector2 import Vector2
import bullet_classes
import explode_class
from random import randint
import prop_classes


# 抽象坦克类
class Tank(tank_sprite.TankSprite):
    def __init__(self, screen):
        tank_sprite.TankSprite.__init__(self, screen)
        self.HP = 0
        # 方向 int 值，对应 pygame 中键盘的上下左右键的值
        self.direction = None
        # 子弹发射的速度
        self.hit_speed = 0
        # 战车移动的速度
        self.move_speed = 0
        # 用于控制射击速度
        self.last_hit_time = 0
        self.last_pos = None
        self.last_rect = None
        # 在地图上的位置
        self.map_pos = None
        self.map_rect = None
        self.last_map_pos = None
        self.last_map_rect = None

    # 产生一辆坦克
    def birth(self):
        pass

    # 发射一颗普通子弹
    def fire(self, current_time, screen_pos):
        if current_time >= self.last_hit_time + self.hit_speed:
            pos = Vector2(0, 0)
            if self.direction == K_UP:
                pos = Vector2(self.position.x, self.position.y - self.frame_height / 2)
            elif self.direction == K_DOWN:
                pos = Vector2(self.position.x, self.position.y + self.frame_height / 2)
            elif self.direction == K_LEFT:
                pos = Vector2(self.position.x - self.frame_width / 2, self.position.y - 8)
            elif self.direction == K_RIGHT:
                pos = Vector2(self.position.x + self.frame_width / 2, self.position.y - 8)
            bullet = bullet_classes.OrdinaryBullet(self.target_surface)
            bullet.fired(pos, self.direction, screen_pos)
            self.last_hit_time = current_time
            return bullet
        else:
            return None

    # 是否死亡
    def is_dead(self):
        if self.HP <= 0:
            return True
        else:
            return False

    # 死亡后产生一次爆炸
    def explode(self):
        explode = explode_class.Explode(self.target_surface)
        explode.fired(self.position)
        return explode

    # 受到伤害
    def hurt(self, num):
        self.HP -= num

    # 转向用于接口
    def change_direction(self, new_direction):
        if self.direction == new_direction:
            return
        self.direction = new_direction

    # 撞墙，停止移动
    def stop(self):
        self.rect = self.last_rect.copy()
        self.position = self.last_pos.copy()
        self.map_pos = self.last_map_pos.copy()
        self.map_rect = self.last_map_rect.copy()

    def get_distance(self, tank):
        distance = self.position.get_distance_to(tank.position)
        return distance


# 玩家坦克类
class PlayerTank(Tank):
    def __init__(self, screen):
        Tank.__init__(self, screen)
        self.HP = 10
        self.hit_speed = 500
        self.special_hit_speed = 1000
        self.move_speed = 100
        self.image_name = "source_material/tanks/player.png"
        self.birth_time = 0
        # 无敌的持续时间（毫秒）
        self.unrivalled_time = 5000
        # 记录剩余特殊子弹的个数
        self.ice_num = 100
        self.fire_num = 100
        self.electricity_num = 100
        # 初始为第6帧
        self.frame = 6
        # 地图大小
        self.map_size = (640, 640)

    def birth(self, pos, current_time, map_pos=Vector2(0, 0)):
        """
        :param pos: 玩家相对于屏幕的出生位置
        :param current_time: 当前时间（毫秒）
        :param map_pos: 玩家相对于地图的出生位置
        :return: void
        """
        self.load(self.image_name, 32, 32, 2)
        self.position = pos
        self.rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.direction = K_UP
        self.birth_time = current_time
        self.map_pos = map_pos
        self.map_rect = Rect(map_pos.x - self.frame_width / 2, map_pos.y - self.frame_height / 2, self.frame_width, self.frame_height)

    # 发射一个特殊子弹
    def fire_a_ice(self, current_time, screen_pos):
        if (current_time >= self.last_hit_time + self.special_hit_speed) and (self.ice_num > 0):
            if self.direction == K_UP:
                pos = Vector2(self.position.x, self.position.y - self.frame_height / 2 - 48)
            elif self.direction == K_DOWN:
                pos = Vector2(self.position.x, self.position.y + self.frame_height / 2 + 48)
            elif self.direction == K_LEFT:
                pos = Vector2(self.position.x - self.frame_width / 2 - 48, self.position.y - 8)
            elif self.direction == K_RIGHT:
                pos = Vector2(self.position.x + self.frame_width / 2 + 48, self.position.y - 8)
            ice = bullet_classes.IceBullet(self.target_surface)
            ice.fired(pos, self.direction, screen_pos)
            self.last_hit_time = current_time
            self.ice_num -= 1
            return ice
        else:
            return None

    def fire_a_fire(self, current_time, screen_pos):
        if (current_time >= self.last_hit_time + self.special_hit_speed) and (self.fire_num > 0):
            if self.direction == K_UP:
                pos = Vector2(self.position.x, self.position.y - self.frame_height / 2 - 48)
            elif self.direction == K_DOWN:
                pos = Vector2(self.position.x, self.position.y + self.frame_height / 2 + 48)
            elif self.direction == K_LEFT:
                pos = Vector2(self.position.x - self.frame_width / 2 - 48, self.position.y - 8)
            elif self.direction == K_RIGHT:
                pos = Vector2(self.position.x + self.frame_width / 2 + 48, self.position.y - 8)
            fire = bullet_classes.FireBullet(self.target_surface)
            fire.fired(pos, self.direction, screen_pos)
            self.last_hit_time = current_time
            self.fire_num -= 1
            return fire
        else:
            return None

    def fire_a_electricity(self, current_time, screen_pos):
        if (current_time >= self.last_hit_time + self.special_hit_speed) and (self.electricity_num > 0):
            if self.direction == K_UP:
                pos = Vector2(self.position.x, self.position.y - self.frame_height / 2 - 48)
            elif self.direction == K_DOWN:
                pos = Vector2(self.position.x, self.position.y + self.frame_height / 2 + 48)
            elif self.direction == K_LEFT:
                pos = Vector2(self.position.x - self.frame_width / 2 - 48, self.position.y - 8)
            elif self.direction == K_RIGHT:
                pos = Vector2(self.position.x + self.frame_width / 2 + 48, self.position.y - 8)
            electricity = bullet_classes.ElectricityBullet(self.target_surface)
            electricity.fired(pos, self.direction, screen_pos)
            self.last_hit_time = current_time
            self.fire_num -= 1
            return electricity
        else:
            return None

    # 因为有无敌效果，重写 hurt 方法
    def hurt(self, num, current_time):
        if current_time - self.birth_time >= self.unrivalled_time:
            self.HP -= num

    def update(self, current_time, time_passed, move_direction, screen_pos, rate=120):
        """
        :param current_time: 当前时间（毫秒）
        :param time_passed: 距离上一次 update 的时间（秒）
        :param move_direction: 键盘接收到后形成的方向向量，二维向量
        :param rate: 变帧的时长（毫秒）
        :return: void
        """
        self.last_map_rect = self.map_rect.copy()
        self.last_map_pos = self.map_pos.copy()
        self.last_pos = self.position.copy()
        self.last_rect = self.rect.copy()
        move_distance = Vector2(self.move_speed * time_passed * move_direction.x, self.move_speed * time_passed * move_direction.y)
        self.map_rect = self.map_rect.move(move_distance.x, move_distance.y)
        self.map_pos.x = (self.map_rect.left + self.map_rect.right) / 2
        self.map_pos.y = (self.map_rect.top + self.map_rect.bottom) / 2
        if (self.map_pos.x < self.target_surface.get_width() / 2) or (self.map_pos.x > (self.map_size[0] - self.target_surface.get_width() / 2)) or (self.map_pos.y < self.target_surface.get_height() / 2) or (self.map_pos.y > (self.map_size[1] - self.target_surface.get_height() / 2)):
            self.position = self.map_pos - screen_pos
        else:
            self.position.x = self.target_surface.get_width() / 2
            self.position.y = self.target_surface.get_height() / 2
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)

        if self.direction == K_DOWN:
            self.frame = 0
        elif self.direction == K_UP:
            self.frame = 6
        elif self.direction == K_LEFT:
            self.frame = 2
        elif self.direction == K_RIGHT:
            self.frame = 4

        if current_time - self.birth_time <= self.unrivalled_time:
            if current_time > (self.last_time + rate):
                if self.frame % 2 == 0:
                    self.frame += 1
                else:
                    self.frame -= 1
                self.last_time = current_time

        frame_x = (self.frame % self.columns) * self.frame_width
        frame_y = (self.frame // self.columns) * self.frame_height
        rect = Rect((frame_x, frame_y, self.frame_width, self.frame_height))
        self.image = self.master_image.subsurface(rect)


# AI坦克类
class AITank(Tank):
    def __init__(self, screen):
        Tank.__init__(self, screen)
        # 添加状态机
        self.brain = state_machine.StateMachine()
        # 为状态机添加状态
        exploring = state_machine.StateExploring(self)
        hitting = state_machine.StateHitting(self)
        turning = state_machine.StateTurning(self)
        self.brain.add_state(exploring)
        self.brain.add_state(hitting)
        self.brain.add_state(turning)
        # 当前属性：paralysis, frozen
        self.state = None
        self.get_state_time = 0
        self.state_keep_time = 5000
        self.view = 200
        # 记录敌人（一个精灵组）
        self.enemies = None
        # 记录是否撞墙
        self.is_strike = False
        # 目标敌机
        self.target = None
        # 子弹精灵
        self.bullet = None

    # 产生一个坦克，随机选择出生地
    def birth(self, pos, group, screen_pos):
        self.load(self.image_name, 32, 32, 3)
        self.map_pos = pos
        self.map_rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.direction = K_UP
        self.brain.set_state("exploring")
        self.enemies = group
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)

    # 获得状态
    def get_state(self, attribute, current_time):
        if attribute == "ice":
            self.state = "frozen"
        if attribute == "electricity":
            self.state = "paralysis"
        self.get_state_time = current_time

    def get_rid_of_state(self, current_time):
        if current_time >= self.get_state_time + self.state_keep_time:
            self.state = None

    def strike(self):
        self.is_strike = True

    def ai_fire(self):
        return self.bullet

    # AI发射一颗子弹
    def fire(self, current_time, screen_pos):
        if current_time >= self.last_hit_time + self.hit_speed:
            pos = Vector2(0, 0)
            if self.direction == K_UP:
                pos = Vector2(self.map_pos.x, self.map_pos.y - self.frame_height / 2)
            elif self.direction == K_DOWN:
                pos = Vector2(self.map_pos.x, self.map_pos.y + self.frame_height / 2)
            elif self.direction == K_LEFT:
                pos = Vector2(self.map_pos.x - self.frame_width / 2, self.map_pos.y - 8)
            elif self.direction == K_RIGHT:
                pos = Vector2(self.map_pos.x + self.frame_width / 2, self.map_pos.y - 8)
            bullet = bullet_classes.AIBullet(self.target_surface)
            bullet.fired(pos, self.direction, screen_pos)
            self.last_hit_time = current_time
            return bullet
        else:
            return None

    def update(self, current_time, time_passed, screen_pos, rate=60):
        self.last_map_rect = self.map_rect.copy()
        self.last_map_pos = self.map_pos.copy()
        self.last_pos = self.position.copy()
        self.last_rect = self.rect.copy()
        if (self.state != "frozen") and (self.state != "paralysis"):
            self.bullet = self.brain.think(current_time, screen_pos)
            if self.direction == K_DOWN:
                self.map_rect = self.map_rect.move(0, self.move_speed * time_passed)
                self.map_pos.y = (self.map_rect.top + self.map_rect.bottom) / 2
                self.frame = 0
            elif self.direction == K_UP:
                self.map_rect = self.map_rect.move(0, -self.move_speed * time_passed)
                self.map_pos.y = (self.map_rect.top + self.map_rect.bottom) / 2
                self.frame = 9
            elif self.direction == K_LEFT:
                self.map_rect = self.map_rect.move(-self.move_speed * time_passed, 0)
                self.map_pos.x = (self.map_rect.left + self.map_rect.right) / 2
                self.frame = 3
            elif self.direction == K_RIGHT:
                self.map_rect = self.map_rect.move(self.move_speed * time_passed, 0)
                self.map_pos.x = (self.map_rect.left + self.map_rect.right) / 2
                self.frame = 6
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)

        if self.state == "paralysis":
            if self.direction == K_DOWN:
                self.frame = 2
            elif self.direction == K_UP:
                self.frame = 11
            elif self.direction == K_LEFT:
                self.frame = 5
            elif self.direction == K_RIGHT:
                self.frame = 8
        elif self.state == "frozen":
            if self.direction == K_DOWN:
                self.frame = 1
            elif self.direction == K_UP:
                self.frame = 10
            elif self.direction == K_LEFT:
                self.frame = 4
            elif self.direction == K_RIGHT:
                self.frame = 7
        frame_x = (self.frame % self.columns) * self.frame_width
        frame_y = (self.frame // self.columns) * self.frame_height
        rect = Rect((frame_x, frame_y, self.frame_width, self.frame_height))
        self.image = self.master_image.subsurface(rect)


# 普通的坦克
class OrdinaryTank(AITank):
    def __init__(self, screen):
        AITank.__init__(self, screen)
        self.HP = 6
        self.move_speed = 80
        self.hit_speed = 1000
        self.image_name = "source_material/tanks/ordinary_car.png"


# 速度型的坦克
class SpeedTank(AITank):
    def __init__(self, screen):
        AITank.__init__(self, screen)
        self.HP = 4
        self.move_speed = 100
        self.hit_speed = 1000
        self.image_name = "source_material/tanks/speed_car.png"


# 重型坦克
class ArmouredTank(AITank):
    def __init__(self, screen):
        AITank.__init__(self, screen)
        self.HP = 10
        self.move_speed = 50
        self.hit_speed = 500
        self.image_name = "source_material/tanks/armoured_car.png"


# 道具车
class PropCar(AITank):
    def __init__(self, screen):
        AITank.__init__(self, screen)
        self.HP = 4
        self.move_speed = 100
        self.image_name = "source_material/tanks/prop_car.png"

    def ai_fire(self):
        pass

    def open(self, current_time):
        c = randint(1, 9)
        if c == 1:
            prop = prop_classes.FireProp(self.target_surface)
            prop.produce(self.position, current_time)
        elif c == 2:
            prop = prop_classes.IceProp(self.target_surface)
            prop.produce(self.position, current_time)
        elif c == 3:
            prop = prop_classes.ElectricityProp(self.target_surface)
            prop.produce(self.position, current_time)
        elif c == 4:
            prop = prop_classes.HitSpeedProp(self.target_surface)
            prop.produce(self.position, current_time)
        elif c == 5:
            prop = prop_classes.HPProp(self.target_surface)
            prop.produce(self.position, current_time)
        elif c == 6:
            prop = prop_classes.BaseHPProp(self.target_surface)
            prop.produce(self.position, current_time)
        elif c == 7:
            prop = prop_classes.LifeProp(self.target_surface)
            prop.produce(self.position, current_time)
        elif c == 8:
            prop = prop_classes.MoveSpeedProp(self.target_surface)
            prop.produce(self.position, current_time)
        elif c == 9:
            prop = prop_classes.CoinProp(self.target_surface)
            prop.produce(self.position, current_time)
        return prop
