from actions.action import Action

class UseItemAction(Action):
    def __init__(self, actor, game, item):
        self.actor = actor
        self.game = game
        self.item = item
        
    def calculate_cost(self):
        return 1000
            
    def do_action(self):
        self.item.use_effect(self.actor, self.game)
        self.actor.timeout += self.calculate_cost()

class GetItemAction(Action):
    def __init__(self, actor, game, tile, item):
        self.actor = actor
        self.game = game
        self.tile = tile
        self.item = item
        
    def calculate_cost(self):
        return 1000
            
    def do_action(self):
        self.tile.remove_item(self.item)
        self.actor.add_to_inventory(self.item)
        self.game.console.add_message("You pick up %s" % self.item.describe())
        self.actor.timeout += self.calculate_cost()
        
class DropItemAction(Action):
    pass
        
    