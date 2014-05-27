from rl import globals as G
from rl.objects import gameobject
from rl.io import colors
from rl.util import dice

class Potion(gameobject.Item):
    usable = True
    char = u'!'
    
    def use_effect(self, actor):
        pass
        
    def throw_effect(self, actor):
        pass
        

class HealingPotion(Potion):
    color = colors.yellow
    name = "healing potion"
    name_plural = "healing potions"
    interest_level = 8
    
    def __init__(self, num=1):
        self.stack_size = num
    
    def use_effect(self, actor):
        actor.heal(dice.d(2, 8))
        G.console.add_message('You feel better.', colors.yellow);
        
        actor.remove_from_inventory(self)
        
