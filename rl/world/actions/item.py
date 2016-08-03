from rl.world.actions import Action
from rl.world.events.items import UseItemEvent, PickUpItemEvent, DropItemEvent


class UseItemAction(Action):
    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

    def cost(self):
        return 1000

    def do_action(self):
        use_events = self.item.use_effect(self.actor)
        UseItemEvent(self.actor, self.item)



class GetItemAction(Action):
    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

    def cost(self):
        return 1000

    def do_action(self):
        self.actor.tile.remove_item(self.item)
        self.actor.inventory.add(self.item)
        return PickUpItemEvent(self.actor, self.item)


class DropItemAction(Action):
    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

    def cost(self):
        return 1000

    def do_action(self):
        item = self.actor.inventory.remove(item=self.item)
        self.actor.tile.add_item(item)
        return DropItemEvent(self.actor, self.item)
