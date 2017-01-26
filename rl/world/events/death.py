from rl.world import events


class DeathEvent(events.Event):
    type = events.EventTypes.death
    def __init__(self, actor):
        self.subject = actor
        # save this because the tile might get cleared out before this has a chance to report
        self.pos = actor.tile.pos

    def perceptible(self, player):
        if self.subject == player:
            return True

        if player.can_see_point(self.pos):
            return True
