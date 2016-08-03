from rl.world.events import Event, EventTypes


class UseItemEvent(Event):
    type = EventTypes.use_item

    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

    def perceptible(self, player):
        return self.actor == player or player.can_see_point(self.actor.tile.pos)

    def describe(self, player):
        if self.actor == player:
            return "You {use} the {item}.".format(
                use=self.item.describe_use(),
                item=self.item.name
            )
        else:
            return "The {actor} {uses} the {item}.".format(
                actor=self.actor.name,
                uses=self.item.describe_use(third_person=True),
                item=self.item.name
            )


class PickUpItemEvent(Event):
    type = EventTypes.get_item

    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

    def perceptible(self, player):
        return self.actor == player or player.can_see_point(self.actor.tile.pos)

    def describe(self, player):
        if self.actor == player:
            return "You pick up a {0}.".format(self.item.name)

        else:
            return "The {0} picks up a {1}.".format(self.actor.name, self.item.name)


class DropItemEvent(Event):
    type = EventTypes.drop_item

    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

    def perceptible(self, player):
        return self.actor == player or player.can_see_point(self.actor.tile.pos)

    def describe(self, player):
        if self.actor == player:
            return "You drop a {0}.".format(self.item.name)

        else:
            return "The {0} drops a {1}.".format(self.actor.name, self.item.name)

