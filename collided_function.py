from pygame.locals import *


def collided_function(sprite1, sprite2):
    if (sprite1.rect.left >= sprite2.rect.left) and (sprite1.rect.left >= sprite2.rect.right):
        return False
    elif (sprite1.rect.left <= sprite2.rect.left) and (sprite1.rect.right <= sprite2.rect.left):
        return False
    elif (sprite1.rect.top >= sprite2.rect.top) and (sprite1.rect.top >= sprite2.rect.bottom):
        return False
    elif (sprite1.rect.top <= sprite2.rect.top) and (sprite1.rect.bottom <= sprite2.rect.top):
        return False
    return True

rect1 = Rect(341, 264, 24, 96)
rect2 = Rect(384, 367, 32, 32)


class MySprite:
    def __init__(self, rect):
        self.rect = rect

sprite_a = MySprite(rect1)
sprite_b = MySprite(rect2)

print(collided_function(sprite_a, sprite_b))
#print(sprite_a.rect.left >= sprite_b.rect.right)
