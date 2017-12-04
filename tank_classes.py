import tank_sprite
import state_machine
from pygame.locals import *
from gameobjects.vector2 import Vector2
import bullet_classes
import explode_class


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

    # 产生一辆坦克
    def birth(self):
        pass

    # 开火
    def fire(self):
        pass

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


class PlayerTank(Tank):
    def __init__(self, screen):
        Tank.__init__(self, screen)
        self.HP = 10
        self.hit_speed = 500
        self.move_speed = 100
        # 用于控制射击速度
        self.last_hit_time = 0
        self.image_name = "source_material/tanks/player.png"
        self.birth_time = 0
        # 无敌的持续时间（毫秒）
        self.unrivalled_time = 5000
        # 记录剩余特殊子弹的个数
        self.ice_num = 0
        self.fire_num = 0
        self.electricity = 0
        # 初始为第6帧
        self.frame = 6
        self.last_pos = None
        self.last_rect = None

    def birth(self, pos, current_time):
        self.load(self.image_name, 32, 32, 2)
        self.position = pos
        self.rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.direction = K_UP
        self.birth_time = current_time

    # 发射一颗普通子弹
    def fire(self, current_time):
        if current_time >= self.last_hit_time + self.hit_speed:
            pos = Vector2(0, 0)
            if self.direction == K_UP:
                pos = Vector2(self.position.x, self.position.y - self.frame_height / 2)
            elif self.direction == K_DOWN:
                pos = Vector2(self.position.x, self.position.y + self.frame_height / 2)
            elif self.direction == K_LEFT:
                pos = Vector2(self.position.x - self.frame_width / 2, self.position.y - 10)
            elif self.direction == K_RIGHT:
                pos = Vector2(self.position.x + self.frame_width / 2, self.position.y - 10)
            bullet = bullet_classes.OrdinaryBullet(self.target_surface)
            print("发射")
            bullet.fired(pos, self.direction)
            self.last_hit_time = current_time
            return bullet
        else:
            return None

    # 发射一个特殊子弹
    def fire_a_ice(self, current_time):
        if (current_time >= self.last_hit_time + self.hit_speed) and (self.ice_num > 0):
            if self.direction == K_UP:
                pos = Vector2(self.position.x, self.position.y - self.frame_height / 2)
            elif self.direction == K_DOWN:
                pos = Vector2(self.position.x, self.position.y + self.frame_height / 2)
            elif self.direction == K_LEFT:
                pos = Vector2(self.position.x - self.frame_width / 2, self.position.y)
            elif self.direction == K_RIGHT:
                pos = Vector2(self.position.x + self.frame_width / 2, self.position.y)
            ice = bullet_classes.IceBullet(self.target_surface)
            ice.fired(pos, self.direction)
            self.last_hit_time = current_time
            self.ice_num -= 1
            return ice
        else:
            return None

    def fire_a_fire(self, current_time):
        if (current_time >= self.last_hit_time + self.hit_speed) and (self.fire_num > 0):
            if self.direction == K_UP:
                pos = Vector2(self.position.x, self.position.y - self.frame_height / 2)
            elif self.direction == K_DOWN:
                pos = Vector2(self.position.x, self.position.y + self.frame_height / 2)
            elif self.direction == K_LEFT:
                pos = Vector2(self.position.x - self.frame_width / 2, self.position.y)
            elif self.direction == K_RIGHT:
                pos = Vector2(self.position.x + self.frame_width / 2, self.position.y)
            fire = bullet_classes.FireBullet(self.target_surface)
            fire.fired(pos, self.direction)
            self.last_hit_time = current_time
            self.fire_num -= 1
            return fire
        else:
            return None

    def fire_a_electricity(self, current_time):
        if (current_time >= self.last_hit_time + self.hit_speed) and (self.fire_num > 0):
            if self.direction == K_UP:
                pos = Vector2(self.position.x, self.position.y - self.frame_height / 2)
            elif self.direction == K_DOWN:
                pos = Vector2(self.position.x, self.position.y + self.frame_height / 2)
            elif self.direction == K_LEFT:
                pos = Vector2(self.position.x - self.frame_width / 2, self.position.y)
            elif self.direction == K_RIGHT:
                pos = Vector2(self.position.x + self.frame_width / 2, self.position.y)
            electricity = bullet_classes.ElectricityBullet(self.target_surface)
            electricity.fired(pos, self.direction)
            self.last_hit_time = current_time
            self.fire_num -= 1
            return electricity
        else:
            return None

    # 撞墙，停止移动
    def stop(self):
        self.rect = self.last_rect
        self.position = self.last_pos

    # 因为有无敌效果，重写 hurt 方法
    def hurt(self, num, current_time):
        if current_time - self.birth_time >= self.unrivalled_time:
            self.HP -= num

    def update(self, current_time, time_passed, move_direction, rate=60):
        self.last_pos = self.position
        self.last_rect = self.rect
        if self.direction == K_DOWN:
            self.rect = self.rect.move(0, self.move_speed * time_passed * move_direction.y)
            self.position.y = (self.rect.top + self.rect.bottom) / 2
            self.frame = 0
        elif self.direction == K_UP:
            self.rect = self.rect.move(0, self.move_speed * time_passed * move_direction.y)
            self.position.y = (self.rect.top + self.rect.bottom) / 2
            self.frame = 6
        elif self.direction == K_LEFT:
            self.rect = self.rect.move(self.move_speed * time_passed * move_direction.x, 0)
            self.position.x = (self.rect.left + self.rect.right) / 2
            self.frame = 2
        elif self.direction == K_RIGHT:
            self.rect = self.rect.move(self.move_speed * time_passed * move_direction.x, 0)
            self.position.x = (self.rect.left + self.rect.right) / 2
            self.frame = 4

        if current_time - self.birth_time <= self.unrivalled_time:
            if self.frame % 2 == 0:
                self.frame += 1
            else:
                self.frame -= 1

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
        self.brain.add_state(exploring)
        self.brain.add_state(hitting)
        # 当前属性：paralysis, frozen
        self.State = None

    # 产生一个坦克，随机选择出生地
    def birth(self):
        pass

    # 获得状态
    def get_state(self):
        pass

    def get_rid_of_stata(self):
        pass
