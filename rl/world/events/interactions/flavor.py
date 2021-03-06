from rl.world.events import Event, EventTypes


class CreatureFlavorEvent(Event):
    type = EventTypes.flavor

    def __init__(self, actor, message):
        self.subject = actor
        self.message = message

    def perceptible(self, player):
        return player.can_see_point(self.subject.tile.pos)

    def describe(self, player):
        return "The {actor} {acts}".format(
            actor=self.subject.name,
            acts=self.message
        )