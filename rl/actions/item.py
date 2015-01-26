from rl import globals as G
from rl.actions.action import Action


class UseItemAction(Action):
    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

    def calculate_cost(self):
        return 1000

    def do_action(self):
        self.item.use_effect(self.actor)
        return True, True


class GetItemAction(Action):
    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

    def calculate_cost(self):
        return 1000

    def do_action(self):
        self.actor.tile.remove_item(self.item)
        self.actor.inventory.add(self.item)
        G.ui.console.add_message("You pick up %s" % self.item.describe())
        return True, True


class DropItemAction(Action):
    def __init__(self, actor, item):
        self.actor = actor
        self.item = item

    def calculate_cost(self):
        return 1000

    def do_action(self):
        item = self.actor.inventory.remove(item=self.item)
        self.actor.tile.add_item(item)
        G.ui.console.add_message("You drop %s." % item.describe())
        return True, True
