import tank_classes
from gameobjects.vector2 import Vector2


# 玩家类，保存一个玩家的基本信息
class Player:
    def __init__(self):
        self.tank = None
        self.life = 3
        self.mark = 0

    def birth_a_tank(self, screen, pos, current_time, map_pos=Vector2(0, 0)):
        if self.life > 0:
            tank = tank_classes.PlayerTank(screen)
            tank.birth(pos, current_time, map_pos)
            self.tank = tank
            self.life -= 1
            return tank
        return None

    def mark_up(self, num):
        self.mark += num

    def get_life(self):
        self.life += 1
