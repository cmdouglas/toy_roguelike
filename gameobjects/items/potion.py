from gameobjects import gameobject
from gameio import colors
from util import dice

class Potion(gameobject.Item):
    usable = True
    char = '!'
    
    def use_effect(self, actor):
        pass
        
    def throw_effect(self, actor):
        pass
        

class HealingPotion(Potion):
    color = colors.yellow
    name = "healing potion"
    name_plural = "healing potions"
    
    def __init__(self, num=1):
        self.stack_size = num
    
    def use_effect(self, actor, game):
        actor.heal(dice.d(2, 8))
        game.console.add_message('You feel better.', colors.yellow);
        
        actor.remove_from_inventory(self)
        
