from rl.events import Event


class LoseHealthEvent(Event):
    pass

class GainHealthEvent(Event):
    def __init__(self, actor, amount):
        self.actor = actor
        self.amount = amount

    def perceptible(self, player):
        return self.actor == player or player.can_see_point(self.actor.tile.pos)

    def describe(self, player):
        if self.actor == player:
            return "You feel better."

        else:
            return "The {0} looks healthier.".format(self.actor.name)