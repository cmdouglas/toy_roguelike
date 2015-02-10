from rl.events import Event


class DeathEvent(Event):
    def __init__(self, actor):
        self.actor = actor

    def describe(self, player):
        if self.actor == player:
            return "You die."

        else:
            return "The {0} dies.".format(self.actor.name)

    def perceptible(self, player):
        if self.actor == player:
            return True

        if player.can_see(self.actor):
            return True
