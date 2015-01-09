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
    def __init__(self, actor, tile, item):
        self.actor = actor
        self.tile = tile
        self.item = item
        
    def calculate_cost(self):
        return 1000
            
    def do_action(self):
        self.tile.remove_item(self.item)
        self.actor.add_to_inventory(self.item)
        G.ui.console.add_message("You pick up %s" % self.item.describe())
        return True, True

class DropItemAction(Action):
    pass
        
    