from rl.world.events import Event, EventTypes


class UseItemEvent(Event):
    type = EventTypes.use_item

    def __init__(self, actor, item):
        self.subject = actor
        self.object = item

    def perceptible(self, player):
        return self.subject == player or player.can_see_point(self.subject.tile.pos)

    def describe(self, player):
        if self.subject == player:
            return "You {use} the {item}.".format(
                use=self.object.describe_use(),
                item=self.object.name
            )
        else:
            return "The {actor} {uses} the {item}.".format(
                actor=self.subject.name,
                uses=self.object.describe_use(third_person=True),
                item=self.object.name
            )


class PickUpItemEvent(Event):
    type = EventTypes.get_item

    def __init__(self, actor, item):
        self.subject = actor
        self.object = item

    def perceptible(self, player):
        return self.subject == player or player.can_see_point(self.subject.tile.pos)

    def describe(self, player):
        if self.subject == player:
            return "You pick up a {0}.".format(self.object.name)

        else:
            return "The {0} picks up a {1}.".format(self.subject.name, self.object.name)


class DropItemEvent(Event):
    type = EventTypes.drop_item

    def __init__(self, actor, item):
        self.subject = actor
        self.object = item

    def perceptible(self, player):
        return self.subject == player or player.can_see_point(self.subject.tile.pos)

    def describe(self, player):
        if self.subject == player:
            return "You drop a {0}.".format(self.object.name)

        else:
            return "The {0} drops a {1}.".format(self.subject.name, self.object.name)

