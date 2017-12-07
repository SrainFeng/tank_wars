import tank_sprite
import pygame
from pygame.locals import *
from gameobjects.vector2 import Vector2


class Bullet(tank_sprite.TankSprite):
    def __init__(self, screen):
        tank_sprite.TankSprite.__init__(self, screen)
        # 子弹的方向
        self.direction = 0
        self.hurt_num = 0
        self.map_pos = None
        self.map_rect = None

    # 产生一颗子弹
    def fired(self):
        pass

    # 子弹自动消失（达到射程或者是帧动画播放完了）
    def is_loss(self):
        pass


# AI子弹
class AIBullet(Bullet):
    def __init__(self, screen):
        Bullet.__init__(self, screen)
        self.hurt_num = 2
        self.fly_speed = 300
        self.fly_distance = 200
        self.image_name = "source_material/bullet/ordinary.png"
        self.birth_pos = None

    def fired(self, pos, direction, screen_pos):
        """
        :param pos: 相对于地图的位置
        :param direction: 方向
        :param screen_pos: 屏幕左上角相对于地图的位置
        :return:
        """
        self.load(self.image_name, 12, 12, 1)
        self.map_pos = pos
        self.map_rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.birth_pos = pos.copy()
        self.direction = direction
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)

    def is_loss(self):
        if (self.map_pos - self.birth_pos).get_length() >= self.fly_distance:
            return True
        else:
            return False

    def update(self, current_time, time_passed, screen_pos, rate=60):
        dire = Vector2(0, 0)
        if self.direction == K_UP:
            dire = Vector2(0, -1)
        elif self.direction == K_DOWN:
            dire = Vector2(0, 1)
        elif self.direction == K_LEFT:
            dire = Vector2(-1, 0)
        elif self.direction == K_RIGHT:
            dire = Vector2(1, 0)
        self.map_rect = self.map_rect.move(self.fly_speed * time_passed * dire.x, self.fly_speed * time_passed * dire.y)
        self.map_pos.x = (self.map_rect.left + self.map_rect.right) / 2
        self.map_pos.y = (self.map_rect.top + self.map_rect.bottom) / 2
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)
        if current_time > (self.last_time + rate):
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.frist_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect((frame_x, frame_y, self.frame_width, self.frame_height))
            image = self.master_image.subsurface(rect)
            if self.direction == K_UP:
                self.image = pygame.transform.rotate(image, 270.)
            elif self.direction == K_DOWN:
                self.image = pygame.transform.rotate(image, 90.)
            elif self.direction == K_LEFT:
                self.image = image
            elif self.direction == K_RIGHT:
                self.image = pygame.transform.rotate(image, 180.)
            self.old_frame = self.frame


# 玩家普通子弹
class OrdinaryBullet(Bullet):
    def __init__(self, screen):
        Bullet.__init__(self, screen)
        self.hurt_num = 2
        self.fly_speed = 300
        self.fly_distance = 200
        self.image_name = "source_material/bullet/ordinary.png"
        self.birth_pos = None

    # 参数为子弹产生的位置
    def fired(self, pos, direction, screen_pos):
        """
        :param pos: 相对于屏幕的位置
        :param direction:
        :param screen_pos:
        :return:
        """
        self.load(self.image_name, 12, 12, 1)
        self.position = pos
        self.rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.birth_pos = pos.copy()
        self.direction = direction
        self.map_pos = self.position + screen_pos
        self.map_rect = Rect(self.map_pos.x - self.frame_width / 2, self.map_pos.y - self.frame_height / 2, self.frame_width, self.frame_height)

    def is_loss(self):
        if (self.position - self.birth_pos).get_length() >= self.fly_distance:
            return True
        else:
            return False

    def update(self, current_time, time_passed, screen_pos, rate=60):
        dire = Vector2(0, 0)
        if self.direction == K_UP:
            dire = Vector2(0, -1)
        elif self.direction == K_DOWN:
            dire = Vector2(0, 1)
        elif self.direction == K_LEFT:
            dire = Vector2(-1, 0)
        elif self.direction == K_RIGHT:
            dire = Vector2(1, 0)
        self.rect = self.rect.move(self.fly_speed * time_passed * dire.x, self.fly_speed * time_passed * dire.y)
        self.position.x = (self.rect.left + self.rect.right) / 2
        self.position.y = (self.rect.top + self.rect.bottom) / 2
        self.map_pos = self.position + screen_pos
        self.map_rect = Rect(self.map_pos.x - self.frame_width / 2, self.map_pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        if current_time > (self.last_time + rate):
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.frist_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect((frame_x, frame_y, self.frame_width, self.frame_height))
            image = self.master_image.subsurface(rect)
            if self.direction == K_UP:
                self.image = pygame.transform.rotate(image, 270.)
            elif self.direction == K_DOWN:
                self.image = pygame.transform.rotate(image, 90.)
            elif self.direction == K_LEFT:
                self.image = image
            elif self.direction == K_RIGHT:
                self.image = pygame.transform.rotate(image, 180.)
            self.old_frame = self.frame


# 特殊子弹的父类
class SpecialBullet(Bullet):
    def __init__(self, screen):
        Bullet.__init__(self, screen)
        self.attribute = None
        self.new = True

    def fired(self, pos, direction, screen_pos):
        self.load(self.image_name, 24, 96, 4)
        self.position = pos
        self.rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.direction = direction
        self.map_pos = self.position + screen_pos
        self.map_rect = Rect(self.map_pos.x - self.frame_width / 2, self.map_pos.y - self.frame_height / 2, self.frame_width, self.frame_height)

    def using(self):
        self.new = False

    def is_new(self):
        return self.new

    def is_loss(self):
        if self.old_frame == self.last_frame:
            return True
        else:
            return False

    def update(self, current_time, screen_pos, rate=200):
        self.map_pos = self.position + screen_pos
        if self.direction == K_UP or self.direction == K_DOWN:
            self.map_rect = Rect(self.map_pos.x - self.frame_width / 2, self.map_pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        elif self.direction == K_LEFT or self.direction == K_RIGHT:
            self.map_rect = Rect(self.map_pos.x - self.frame_width / 2, self.map_pos.y - self.frame_height / 2, self.frame_height, self.frame_width)
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.frist_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect((frame_x, frame_y, self.frame_width, self.frame_height))
            image = self.master_image.subsurface(rect)
            if self.direction == K_UP:
                self.image = pygame.transform.rotate(image, 180.)
                self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)
            elif self.direction == K_DOWN:
                self.image = image
                self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)
            elif self.direction == K_LEFT:
                self.image = pygame.transform.rotate(image, 270.)
                self.rect = Rect(self.position.x - self.frame_height / 2, self.position.y - self.frame_width / 2, self.frame_height, self.frame_width)
            elif self.direction == K_RIGHT:
                self.image = pygame.transform.rotate(image, 90.)
                self.rect = Rect(self.position.x - self.frame_height / 2, self.position.y - self.frame_width / 2, self.frame_height, self.frame_width)
            self.old_frame = self.frame


# 火焰弹类
class FireBullet(SpecialBullet):
    def __init__(self, screen):
        SpecialBullet.__init__(self, screen)
        self.image_name = "source_material/bullet/fire.png"
        self.hurt_num = 4
        self.attribute = "fire"


# 冰弹类
class IceBullet(SpecialBullet):
    def __init__(self, screen):
        SpecialBullet.__init__(self, screen)
        self.image_name = "source_material/bullet/ice.png"
        self.hurt_num = 2
        self.attribute = "ice"


# 电弹类
class ElectricityBullet(SpecialBullet):
    def __init__(self, screen):
        SpecialBullet.__init__(self, screen)
        self.image_name = "source_material/bullet/electricity.png"
        self.hurt_num = 2
        self.attribute = "electricity"
