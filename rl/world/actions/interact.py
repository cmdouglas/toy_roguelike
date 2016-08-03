import logging
from rl.world.actions import Action
from rl.world.events.interactions.combat import CombatEvent
from rl.world.events.interactions.misc import ExamineEvent, OpenEvent, CloseEvent
from rl.world.combat import fight

logger = logging.getLogger('rl')


class AttackAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def cost(self):
        return 1000

    def do_action(self):
        attack_result = fight(self.actor, self.other)

        return attack_result


class ExamineAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def cost(self):
        return 0

    def do_action(self):
        return ExamineEvent(self.actor, self.other)


class OpenAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def cost(self):
        return 1000

    def do_action(self):
        # opening a door can cause entities to shift around
        tile = self.other.tile

        self.other.open()
        return OpenEvent(self.actor, tile.terrain)


class CloseAction(Action):
    def __init__(self, actor, other):
        self.actor = actor
        self.other = other

    def cost(self):
        return 1000

    def do_action(self):
        # closing a door can cause entities to shift around
        tile = self.other.tile

        self.other.close()
        return CloseEvent(self.actor, tile.terrain)
