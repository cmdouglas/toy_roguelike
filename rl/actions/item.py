from rl.actions.action import Action
from rl.events.items import UseItemEvent, PickUpItemEvent, DropItemEvent


class UseItemAction(Action):
    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

    def calculate_cost(self):
        return 1000

    def do_action(self):
        use_events = self.item.use_effect(self.actor)
        r = [UseItemEvent(self.actor, self.item)]
        r.extend(use_events)
        return r

class GetItemAction(Action):
    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

    def calculate_cost(self):
        return 1000

    def do_action(self):
        self.actor.tile.remove_item(self.item)
        self.actor.inventory.add(self.item)
        return [PickUpItemEvent(self.actor, self.item)]

class DropItemAction(Action):
    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

    def calculate_cost(self):
        return 1000

    def do_action(self):
        pos = self.actor.tile.pos
        item = self.actor.inventory.remove(item=self.item)
        self.actor.tile.board.add_entity(item, pos)
        return [DropItemEvent(self.actor, self.item)]
