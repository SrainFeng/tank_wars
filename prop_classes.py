import tank_sprite
from pygame.locals import *


class Prop(tank_sprite.TankSprite):
    def __init__(self, screen):
        tank_sprite.TankSprite.__init__(self, screen)
        # 道具存在的时间
        self.keep_time = 0
        self.birth_time = 0
        # 记录位置，为二维向量
        self.map_pos = None
        self.map_rect = None
        self.prop_name = None

    # 产生一个道具，参数为生成的坐标
    def produce(self):
        pass

    # 道具自动消失（存在时限到）
    def is_loss(self, current_time):
        if current_time - self.birth_time >= self.keep_time:
            return True
        else:
            return False

    def update(self, current_time, screen_pos, rate=90):
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)
        if current_time - self.last_time >= rate:
            self.frame += 1
            if self.frame == self.last_frame:
                self.frame = self.frist_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect((frame_x, frame_y, self.frame_width,self.frame_height))
            self.image = self.master_image.subsurface(rect)


# 攻击道具的父类（各种特殊子弹以及射速提升道具）
class AttackProp(Prop):
    def __init__(self, screen):
        Prop.__init__(self, screen)
        self.keep_time = 25000

    def produce(self, pos, current_time, screen_pos):
        """
        :param pos: 滚动地图中，该对象相对于地图坐标系的位置
        :param current_time: 当前时间
        :param screen_pos: 目前显示屏幕的左上角相对于地图坐标系的位置
        :return: void
        """
        self.load(self.image_name, 32, 32, 3)
        self.map_pos = pos
        self.map_rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.birth_time = current_time
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)


# 各种其他道具的父类（坦克回复、生命和移速；基地回复；金币）
class OtherProp(Prop):
    def __init__(self, screen):
        Prop.__init__(self, screen)
        self.keep_time = 20000

    def produce(self, pos, current_time, screen_pos):
        self.load(self.image_name, 32, 32, 4)
        self.map_pos = pos
        self.map_rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.birth_time = current_time
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)


# 电弹道具
class ElectricityProp(AttackProp):
    def __init__(self, screen):
        AttackProp.__init__(self, screen)
        self.image_name = "source_material/prop/electricity.png"
        self.prop_name = "electricity"


# 火焰弹道具
class FireProp(AttackProp):
    def __init__(self, screen):
        AttackProp.__init__(self, screen)
        self.image_name = "source_material/prop/fire.png"
        self.prop_name = "fire"


# 冰弹道具
class IceProp(AttackProp):
    def __init__(self, screen):
        AttackProp.__init__(self, screen)
        self.image_name = "source_material/prop/ice.png"
        self.prop_name = "ice"


# 攻速加成道具
class HitSpeedProp(AttackProp):
    def __init__(self, screen):
        AttackProp.__init__(self, screen)
        self.image_name = "source_material/prop/hit_speed.png"
        self.prop_name = "hit_speed"


# HP回复道具
class HPProp(OtherProp):
    def __init__(self, screen):
        OtherProp.__init__(self, screen)
        self.image_name = "source_material/prop/HP.png"
        self.prop_name = "HP"


# 生命数增加道具
class LifeProp(OtherProp):
    def __init__(self, screen):
        OtherProp.__init__(self, screen)
        self.image_name = "source_material/prop/life.png"
        self.prop_name = "life"


# 移速加成道具
class MoveSpeedProp(OtherProp):
    def __init__(self, screen):
        OtherProp.__init__(self, screen)
        self.image_name = "source_material/prop/move_speed.png"
        self.prop_name = "move_speed"


# 基地HP回复道具
class BaseHPProp(OtherProp):
    def __init__(self, screen):
        OtherProp.__init__(self, screen)
        self.image_name = "source_material/prop/base_HP.png"
        self.prop_name = "base_HP"


# 金币道具
class CoinProp(OtherProp):
    def __init__(self, screen):
        OtherProp.__init__(self, screen)
        self.image_name = "source_material/prop/coin.png"
        self.prop_name = "coin"
