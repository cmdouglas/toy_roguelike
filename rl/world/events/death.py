from rl.world.events import Event


class DeathEvent(Event):
    def __init__(self, actor):
        self.actor = actor
        # save this because the tile might get cleared out before this has a chance to report
        self.pos = actor.tile.pos

    def describe(self, player):
        if self.actor == player:
            return "You die."

        else:
            return "The {0} dies.".format(self.actor.name)

    def perceptible(self, player):
        if self.actor == player:
            return True

        if player.can_see_point(self.pos):
            return True
