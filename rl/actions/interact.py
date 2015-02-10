from rl.actions.action import Action
from rl.events.interactions.combat import AttackEvent
from rl.events.interactions.misc import ExamineEvent, OpenEvent, CloseEvent


class AttackAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other
        
    def calculate_cost(self):
        return 1000
            
    def do_action(self):
        attack_result = self.actor.attack(self.other)
        return [AttackEvent(self.actor, self.other)].extend(attack_result)


class ExamineAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def calculate_cost(self):
        return 0

    def do_action(self):
        self.actor.timeout += self.calculate_cost()

        return [ExamineEvent(self.actor, self.other)]

class OpenAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def calculate_cost(self):
        return 1000

    def do_action(self):
        self.other.open()
        return [OpenEvent(self.actor, self.other)]


class CloseAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def calculate_cost(self):
        return 1000

    def do_action(self):
        self.other.close()
        return [CloseEvent(self.actor, self.other)]


