import tank_sprite
import state_machine


# 抽象坦克类
class Tank(tank_sprite.TankSprite):
    def __init__(self, screen):
        tank_sprite.TankSprite.__init__(self, screen)
        self.Hp = 0
        # 方向 up, down, left, right
        self.direction = None
        self.hit_speed = 0
        self.move_speed = 0

    # 开火
    def fire(self):
        pass

    # 死亡
    def dead(self):
        pass

    # 受到伤害
    def hurted(self, num):
        self.Hp -= num

    def update(self):
        pass

    # 活动过程
    def process(self, time_passed):
        pass


# AI坦克类
class AITank(Tank):
    def __init__(self, screen):
        Tank.__init__(self,screen)
        # 添加状态机
        self.brain = state_machine.StateMachine()
        # 为状态机添加状态
        exploring = state_machine.StateExploring(self)
        hitting = state_machine.StateHitting(self)
        self.brain.add_state(exploring)
        self.brain.add_state(hitting)
        # 当前属性：paralysis, frozen
        self.State = None

    # 产生一个坦克，随机选择出生地
    def birth(self):
        pass

    # 获得状态
    def get_state(self):
        pass

    def get_rid_of_stata(self):
        pass
