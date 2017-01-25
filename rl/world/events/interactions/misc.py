from rl.world.events import Event, EventTypes


class ExamineEvent(Event):
    type = EventTypes.examine

    def __init__(self, examiner, obj):
        self.subject = examiner
        self.object = obj

    def describe(self, player):
        return self.object.description

    def perceptible(self, player):
        return True


class OpenEvent(Event):
    type = EventTypes.open

    def __init__(self, opener, openee):
        self.subject = opener
        self.object = openee

    def describe(self, player):
        if self.subject == player:
            return "You open the {0}".format(self.object.name)

        if player.can_see_point(self.subject.tile.pos):
            return "The {0} opens the {1}".format(self.subject.name, self.object.name)

        return "The {0} opens.".format(self.object.name)

    def perceptible(self, player):
        return self.subject is player or player.can_see_point(self.object.tile.pos)


class CloseEvent(Event):
    type = EventTypes.close

    def __init__(self, closer, closee):
        self.subject = closer
        self.object = closee

    def describe(self, player):
        if self.subject == player:
            return "You close the {0}".format(self.object.name)

        if player.can_see_point(self.subject.tile.pos):
            return "The {0} closes the {1}".format(self.subject.name, self.object.name)

        return "The {0} closes.".format(self.object.name)

    def perceptible(self, player):
        return self.subject is player or player.can_see_point(self.object.tile.pos)
