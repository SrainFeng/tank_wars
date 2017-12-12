import hinder_classes
from pygame.locals import *
import explode_class


# 基地对象,继承自可破坏障碍物类
class Base(hinder_classes.Box):
    def __init__(self, screen):
        hinder_classes.Box.__init__(self, screen)
        self.HP = 40
        self.image_name = "source_material/hinder/base.png"
        self.screen_pos

    def put(self, pos, screen_pos):
        self.load(self.image_name, 81, 64, 1)
        self.map_pos = pos
        self.map_rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.image = self.master_image
        self.screen_pos = screen_pos
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)

    def hurt(self, num):
        self.HP -= num

    def hp_up(self, num):
        self.HP += num
        if self.HP > 40:
            self.HP = 40

    def explode(self):
        explode = explode_class.Explode(self.target_surface)
        explode.fired(self.map_pos, self.screen_pos)
        return explode

    def update(self, screen_pos):
        self.screen_pos = screen_pos
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)
