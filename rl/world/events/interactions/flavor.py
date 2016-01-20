from rl.world.events import Event


class CreatureFlavorEvent(Event):
    """The goblin scratches its head or whatever"""
    def __init__(self, actor, message):
        self.actor = actor
        self.message = message

    def perceptible(self, player):
        return player.can_see_point(self.actor.tile.pos)

    def describe(self, player):
        return "The {actor} {acts}".format(
            actor=self.actor.name,
            acts=self.message
        )