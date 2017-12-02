class StateMachine:
    def __init__(self):
        self.states = {}
        self.active_state = None

    # 为实体添加其会拥有的状态
    def add_state(self, state):

        self.states[state.name] = state

    def think(self):
        if self.active_state is None:
            return
        self.active_state.do_actions()
        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)

    # 更新状态
    def set_state(self, new_state_name):
        if self.active_state is not None:
            self.active_state.exit_actions()
        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()


class State:
    def __init__(self,name):
        self.name = name

    def do_actions(self):
        pass

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class StateExploring(State):
    def __init__(self, tank):
        State.__init__(self, "exploring")
        self.tank = tank


class StateHitting(State):
    def __init__(self, tank):
        State.__init__(self, "hitting")
        self.tank = tank
        self.loss = False
