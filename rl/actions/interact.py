from rl import globals as G
from rl.actions.action import Action

class AttackAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other
        
    def calculate_cost(self):
        return 1000
            
    def do_action(self):
        effect = self.actor.is_in_fov() or self.other.is_in_fov()
        self.actor.attack(self.other)
        return True, effect

class ExamineAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def calculate_cost(self):
        return 0

    def do_action(self):
        self.actor.timeout += self.calculate_cost()
        effect = False
        if self.other.description:
            effect = True
            G.ui.console.add_message(self.other.description)

        return True, effect

class OpenAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def calculate_cost(self):
        return 1000

    def do_action(self):
        effect = self.actor.is_in_fov() or self.other.is_in_fov()
        self.other.open()

        return True, effect

class CloseAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def calculate_cost(self):
        return 1000

    def do_action(self):
        effect = self.actor.is_in_fov() or self.other.is_in_fov()

        self.other.close()
        return True, effect



