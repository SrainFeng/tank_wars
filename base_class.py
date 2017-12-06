import hinder_classes
from pygame.locals import *
import explode_class


# 基地对象,继承自可破坏障碍物类
class Base(hinder_classes.DestroyableHinder):
    def __init__(self, screen):
        hinder_classes.DestroyableHinder.__init__(self, screen)
        self.HP = 40
        self.image_name = "source_material/hinder/base.png"

    def put(self, pos):
        self.load(self.image_name, 81, 64, 1)
        self.position = pos
        self.rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.image = self.master_image

    def explode(self):
        explode = explode_class.Explode(self.target_surface)
        explode.fired(self.position)
        return explode
