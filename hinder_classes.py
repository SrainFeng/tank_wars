import tank_sprite
from pygame.locals import *
import prop_classes
from random import randint


# 可破坏的障碍物
class Box(tank_sprite.TankSprite):
    def __init__(self, screen):
        tank_sprite.TankSprite.__init__(self, screen)
        self.HP = 4
        self.map_pos = None
        self.map_rect = None
        self.screen_pos = None
        self.image = self.master_image

    def put(self, pos, screen_pos):
        """
        :param pos: 滚动地图中，该对象相对于地图坐标系的位置
        :param screen_pos: 目前显示屏幕的左上角相对于地图坐标系的位置
        :return: void
        """
        self.load(self.image_name, 32, 32, 1)
        self.map_pos = pos
        self.map_rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.image = self.master_image
        self.screen_pos = screen_pos
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)

    # 是否被破坏
    def is_destroyed(self):
        if self.HP <= 0:
            return True
        else:
            return False

    # 箱子被破坏，随机产生一个道具
    def open(self):
        pass

    # 受到伤害
    def hurt(self, num):
        self.HP -= num

    def update(self, screen_pos):
        self.screen_pos = screen_pos
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)


# 武器补给箱
class AmmunitionSupplyBox(Box):
    def __init__(self, screen):
        Box.__init__(self, screen)
        self.image_name = "source_material/hinder/ammunition_supply_box.png"

    def open(self, current_time):
        c = randint(1, 4)
        if c == 1:
            prop = prop_classes.FireProp(self.target_surface)
            prop.produce(self.map_pos, current_time, self.screen_pos)
        elif c == 2:
            prop = prop_classes.IceProp(self.target_surface)
            prop.produce(self.map_pos, current_time, self.screen_pos)
        elif c == 3:
            prop = prop_classes.ElectricityProp(self.target_surface)
            prop.produce(self.map_pos, current_time, self.screen_pos)
        elif c == 4:
            prop = prop_classes.HitSpeedProp(self.target_surface)
            prop.produce(self.map_pos, current_time, self.screen_pos)
        return prop


# 医疗补给箱
class MedicineSupplyBox(Box):
    def __init__(self, screen):
        Box.__init__(self, screen)
        self.image_name = "source_material/hinder/medicine_supply_box.png"

    def open(self, current_time):
        c = randint(1, 4)
        if c == 1:
            prop = prop_classes.HPProp(self.target_surface)
            prop.produce(self.map_pos, current_time, self.screen_pos)
        elif c == 2:
            prop = prop_classes.BaseHPProp(self.target_surface)
            prop.produce(self.map_pos, current_time, self.screen_pos)
        elif c == 3:
            prop = prop_classes.LifeProp(self.target_surface)
            prop.produce(self.map_pos, current_time, self.screen_pos)
        elif c == 4:
            prop = prop_classes.MoveSpeedProp(self.target_surface)
            prop.produce(self.map_pos, current_time, self.screen_pos)
        return prop

'''
# 不可破坏的障碍物
class DisDestroyableHinder(Hinder):
    def __init__(self, screen):
        Hinder.__init__(screen)


# 石柱
class PineTree(DisDestroyableHinder):
    def __init__(self, screen):
        DisDestroyableHinder.__init__(self, screen)
        self.image_name = "source_material/hinder/stone.png"

    def put(self, pos):
        self.load(self.image_name, 64, 110, 1)
        self.position = pos
        self.rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.image = self.master_image


# 灌木
class Bush(DisDestroyableHinder):
    def __init__(self, screen):
        DisDestroyableHinder.__init__(self, screen)
        self.image_name = "source_material/hinder/bush.png"

    def put(self, pos):
        self.load(self.image_name, 64, 64, 1)
        self.position = pos
        self.rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, pos.x + self.frame_width / 2, pos.y + self.frame_height / 2)
        self.image = self.master_image


# 土坑
class Pit(DisDestroyableHinder):
    def __init__(self, screen):
        DisDestroyableHinder.__init__(self, screen)
        self.image_name = "source_material/hinder/pit.png"

    def put(self, pos):
        self.load(self.image_name, 128, 128, 1)
        self.position = pos
        self.rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, pos.x + self.frame_width / 2, pos.y + self.frame_height / 2)
        self.image = self.master_image
'''
