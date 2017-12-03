import tank_sprite
import pygame
from pygame.locals import *
from gameobjects.vector2 import Vector2
OrdinaryBullet = "source_material/bullet/Ordinary.png"


class Bullet(tank_sprite.TankSprite):
    def __init__(self, screen):
        tank_sprite.TankSprite.__init__(self, screen)
        self.hurt_num = 0
        self.fly_speed = 0
        self.fly_time = 0

    # 产生一颗子弹
    def fired(self):
        pass

    # 子弹自动消失（达到射程或者是帧动画播放完了）
    def loss(self):
        pass


# 普通子弹
class OrdinaryBullet(Bullet):
    def __init__(self, screen):
        Bullet.__init__(self, screen)
        self.hurt_num = 2
        self.fly_speed = 300
        self.fly_distance = 200
        self.image_name = "source_material/bullet/ordinary.png"
        self.birth_pos = None

    # 参数为子弹产生的位置
    def fired(self, pos_x, pos_y):
        self.load(self.image_name, 12, 12, 1)
        self.position = Vector2(pos_x, pos_y)
        self.rect = Rect(pos_x - self.frame_width / 2, pos_y - self.frame_height / 2, pos_x + self.frame_width / 2, pos_y + self.frame_height / 2)
        self.birth_pos = Vector2(pos_x, pos_y)

    def loss(self):
        if (self.position - self.birth_pos).get_length() >= self.fly_distance:
            return True
        else:
            return False

    # 根据 direction 参数确定发射方向
    def update(self, current_time, time_passed, direction, rate=60):
        if direction == "up":
            dire = Vector2(0, -1)
        elif direction == "down":
            dire = Vector2(0, 1)
        elif direction == "left":
            dire = Vector2(-1, 0)
        elif direction == "right":
            dire = Vector2(1, 0)
        self.position.x += self.fly_speed * time_passed * dire.x
        self.position.y += self.fly_speed * time_passed * dire.y
        center = Vector2(self.frame_width / 2, self.frame_height / 2)
        self.rect = self.position.x - center.x, self.position.y - center.y, self.position.x + center.x, self.position.y + center.y
        if current_time > (self.last_time + rate):
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.frist_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect((frame_x, frame_y, self.frame_width,self.frame_height))
            image = self.master_image.subsurface(rect)
            if direction == "up":
                self.image = pygame.transform.rotate(image, 270.)
            elif direction == "down":
                self.image = pygame.transform.rotate(image, 90.)
            elif direction == "left":
                self.image = image
            elif direction == "right":
                self.image = pygame.transform.rotate(image, 180.)
            self.old_frame = self.frame


# 特殊子弹的父类
class SpecialBullet(Bullet):
    def __init__(self, screen):
        Bullet.__init__(self, screen)
        self.hurt_num = 2

    def fired(self, pos_x, pos_y):
        self.load(self.image_name, 24, 96, 4)
        self.position = Vector2(pos_x, pos_y)
        self.rect = Rect(pos_x - self.frame_width / 2, pos_y, pos_x + self.frame_width / 2, pos_y + self.frame_height)

    def loss(self):
        if self.old_frame == self.last_frame:
            return True
        else:
            return False

    def update(self, current_time, direction, rate=120):
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.frist_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect((frame_x, frame_y, self.frame_width,self.frame_height))
            image = self.master_image.subsurface(rect)
            if direction == "up":
                self.image = pygame.transform.rotate(image, 180.)
                self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height, self.position.x + self.frame_width / 2, self.position.y)
            elif direction == "down":
                self.image = image
            elif direction == "left":
                self.image = pygame.transform.rotate(image, 270.)
                self.rect = Rect(self.position.x - self.frame_height, self.position.y - self.frame_width / 2, self.position.x, self.position.y + self.frame_width / 2)
            elif direction == "right":
                self.image = pygame.transform.rotate(image, 90.)
                self.rect = Rect(self.position.x, self.position.y - self.frame_width / 2, self.position.x + self.frame_height, self.position.y + self.frame_width / 2)
            self.old_frame = self.frame


# 火焰弹类
class FireBullet(SpecialBullet):
    def __init__(self, screen):
        SpecialBullet.__init__(self, screen)
        self.image_name = "source_material/bullet/fire.png"


# 冰弹类
class IceBullet(SpecialBullet):
    def __init__(self, screen):
        SpecialBullet.__init__(self, screen)
        self.image_name = "source_material/bullet/ice.png"


# 电弹类
class ElectricityBullet(SpecialBullet):
    def __init__(self, screen):
        SpecialBullet.__init__(self, screen)
        self.image_name = "source_material/bullet/electricity.png"
