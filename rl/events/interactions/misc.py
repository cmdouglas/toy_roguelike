from rl.events import Event

class ExamineEvent(Event):
    def __init__(self, examiner, obj):
        self.examiner = examiner
        self.obj = obj

    def describe(self, player):
        return self.obj.description

    def perceptible(self, player):
        return True


class OpenEvent(Event):
    def __init__(self, opener, openee):
        self.opener = opener
        self.openee = openee

    def describe(self, player):
        if self.opener == player:
            return "You open the {0}".format(self.openee.name)

        if player.can_see_point(self.opener.tile.pos):
            return "The {0} opens the {1}".format(self.opener.name, self.openee.name)

        return "The {0} opens.".format(self.openee.name)

    def perceptible(self, player):
        return self.opener is player or player.can_see_point(self.openee.tile.pos)


class CloseEvent(Event):
    def __init__(self, closer, closee):
        self.closer = closer
        self.closee = closee

    def describe(self, player):
        if self.closer == player:
            return "You close the {0}".format(self.closee.name)

        if player.can_see_point(self.closer.tile.pos):
            return "The {0} closes the {1}".format(self.closer.name, self.closee.name)

        return "The {0} closes.".format(self.closee.name)

    def perceptible(self, player):
        return self.closer is player or player.can_see_point(self.closee.tile.pos)
