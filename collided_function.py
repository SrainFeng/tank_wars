from pygame.locals import *


def collided_function(sprite1, sprite2):
    if (sprite1.rect.left >= sprite2.rect.left) and (sprite1.rect.left >= sprite2.rect.right):
        return False
    elif (sprite1.rect.left <= sprite2.rect.left) and (sprite1.rect.right <= sprite2.rect.left):
        return False
    elif (sprite1.rect.top >= sprite2.rect.top) and (sprite1.rect.top <= sprite2.rect.bottom):
        return False
    elif (sprite1.rect.top <= sprite2.rect.top) and (sprite1.rect.bottom <= sprite2.rect.top):
        return False
    return True

rect1 = Rect(282, 208, 64, 64)
rect2 = Rect(529, 231, 12, 12)


class Sprite:
    def __init__(self, rect):
        self.rect = rect

sprite_a = Sprite(rect1)
sprite_b = Sprite(rect2)
print(collided_function(sprite_a, sprite_a))
