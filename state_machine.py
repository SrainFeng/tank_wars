from random import randint
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT


class StateMachine:
    def __init__(self):
        self.states = {}
        self.active_state = None

    # 为实体添加其会拥有的状态
    def add_state(self, state):

        self.states[state.name] = state

    def think(self, current_time):
        if self.active_state is None:
            return
        bullet = self.active_state.do_actions(current_time)
        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)
        if bullet:
            return bullet

    # 更新状态
    def set_state(self, new_state_name):
        if self.active_state is not None:
            self.active_state.exit_actions()
        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()


class State:
    def __init__(self,name):
        self.name = name

    def do_actions(self, current_time):
        pass

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


# 巡逻状态
class StateExploring(State):
    def __init__(self, tank):
        State.__init__(self, "exploring")
        self.tank = tank

    def random_direction(self):
        c = randint(0, 3)
        if c == 0:
            self.tank.direction = K_UP
        elif c == 1:
            self.tank.direction = K_DOWN
        elif c == 2:
            self.tank.direction = K_LEFT
        elif c == 3:
            self.tank.direction = K_RIGHT

    def do_actions(self, current_time):
        if randint(1, 100) == 1:
            self.random_direction()

    def check_conditions(self):
        for enemy in self.tank.enemies:
            if self.tank.get_distance(enemy) <= self.tank.view:
                self.tank.target = enemy
                return "hitting"
        if self.tank.is_strike:
            self.tank.is_strike = False
            return "turning"
        return None

    def entry_actions(self):
        self.random_direction()


# 攻击状态
class StateHitting(State):
    def __init__(self, tank):
        State.__init__(self, "hitting")
        self.tank = tank

    def do_actions(self, current_time):
        bullet = self.tank.fire(current_time)
        return bullet

    def check_conditions(self):
        if self.tank.is_strike:
            self.tank.is_strike = False
            return "turning"
        if self.tank.get_distance(self.tank.target) > self.tank.view:
            self.tank.target = None
            return "exploring"
        if self.tank.target.is_dead():
            return "exploring"


# 转向状态
class StateTurning(State):
    def __init__(self, tank):
        State.__init__(self, "turning")
        self.tank = tank

    def do_actions(self, current_time):
        self.tank.direction += 1
        if self.tank.direction > 276:
            self.tank.direction -= 4

    def check_conditions(self):
        return "exploring"
