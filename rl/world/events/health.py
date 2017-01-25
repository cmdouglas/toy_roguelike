from rl.world import events


class GainHealthEvent(events.Event):
    type = events.EventTypes.gain_health

    def __init__(self, actor, amount):
        self.subject = actor
        self.amount = amount

    def perceptible(self, player):
        return self.subject == player or player.can_see_point(self.subject.tile.pos)

    def describe(self, player):
        if self.subject == player:
            return "You feel better."

        else:
            return "The {0} looks healthier.".format(self.subject.name)


class LoseHealthEvent(events.Event):
    type = events.EventTypes.lose_health

    def __init__(self, actor, amount):
        self.subject = actor
        self.amount = amount

    def perceptible(self, player):
        return self.subject == player
