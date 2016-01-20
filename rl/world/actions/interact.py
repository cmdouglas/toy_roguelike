import logging
from rl.world.actions import Action
from rl.world.events.interactions.combat import AttackEvent
from rl.world.events.interactions.misc import ExamineEvent, OpenEvent, CloseEvent


logger = logging.getLogger('rl')

class AttackAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other
        
    def calculate_cost(self):
        return 1000
            
    def do_action(self):
        attack_result = self.actor.attack(self.other)

        return attack_result


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


