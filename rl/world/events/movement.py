from rl.world.events import Event, EventTypes


class MoveEvent(Event):
    type = EventTypes.move

    def __init__(self, actor, from_pos, to_pos):
        self.subject = actor
        self.from_pos = from_pos
        self.to_pos = to_pos

    def perceptible(self, player):
        return self.subject == player or player.can_see_point(self.from_pos) or player.can_see_point(self.to_pos)


class WaitEvent(Event):
    type = EventTypes.wait

    def __init__(self, actor):
        self.subject = actor


class TeleportEvent(MoveEvent):
    type = EventTypes.teleport

    def perceptible(self, player):
        return self.subject == player or player.can_see_point(self.from_pos) or player.can_see_point(self.to_pos)

    def describe(self, player):
        if self.subject == player:
            return "You teleport."

        elif player.can_see_point(self.from_pos) and player.can_see_point(self.to_pos):
            return "The {0} teleports.".format(self.subject.name)

        elif player.can_see_point(self.from_pos):
            return "The {0} vanishes!".format(self.subject.name)

        elif player.can_see_point(self.to_pos):
            return "Suddenly, a {0} appears!".format(self.subject.name)