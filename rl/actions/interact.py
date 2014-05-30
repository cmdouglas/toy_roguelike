from rl import globals as G
from rl.actions.action import Action

class AttackAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other
        
    def calculate_cost(self):
        return 1000
            
    def do_action(self):
        self.actor.timeout += self.calculate_cost()
        self.actor.attack(self.other)

class ExamineAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def calculate_cost(self):
        return 0

    def do_action(self):
        self.actor.timeout += self.calculate_cost()
        if self.other.description:
            G.console.add_message(self.other.description)

class OpenAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def calculate_cost(self):
        return 1000

    def do_action(self):
        self.other.open()

class CloseAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def calculate_cost(self):
        return 1000

    def do_action(self):
        self.other.close()



