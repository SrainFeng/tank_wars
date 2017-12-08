import tank_sprite
from pygame.locals import *
from gameobjects.vector2 import Vector2


class Explode(tank_sprite.TankSprite):
    def __init__(self, screen):
        tank_sprite.TankSprite.__init__(self, screen)
        self.image_name = "source_material/explode/explode.png"
        self.map_pos = None
        self.map_rect = None

    def fired(self, pos, screen_pos):
        self.load(self.image_name, 64, 64, 4)
        self.map_pos = Vector2(pos.x, pos.y)
        self.map_rect = Rect(pos.x - self.frame_width / 2, pos.y - self.frame_height / 2, self.frame_width, self.frame_height)
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)

    def is_loss(self):
        if self.old_frame == self.last_frame:
            return True
        else:
            return False

    def update(self, current_time, screen_pos, rate=120):
        self.position = self.map_pos - screen_pos
        self.rect = Rect(self.position.x - self.frame_width / 2, self.position.y - self.frame_height / 2, self.frame_width, self.frame_height)
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.frist_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect((frame_x, frame_y, self.frame_width, self.frame_height))
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame
