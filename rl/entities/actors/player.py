import time

from rl import globals as G
from rl.ui import colors
from rl.util import dice

from rl.entities.actors.mob import Mob
from rl.entities.items import potion

class Player(Mob):
    def __init__(self):
        self.color = colors.bright_white
        self.char = u'@'
        self.sight_radius = 10
        self.name = u"Charlie"
        self.level = 1
        self.health = 20
        self.max_health = 20
        self.energy = 10
        self.max_energy = 10
        self.str = 8
        self.mag = 15
        self.dex = 10
        self.gold = 300
        self.is_alive = True
        
        self.inventory = {
            'a': potion.HealingPotion(num=3)
        }
        
        self.queued_actions = []
    
    def on_move(self, dx, dy):
        self.tile.board.show_player_fov()
        self.tile.visible=True
    
    def queue_action(self, action):
        self.queued_actions.append(action)
    
    def process_turn(self):
        if dice.one_chance_in(6):
            self.heal(1)
                
    def emote(self, message, color=None):
        if not color:
            color = self.color
        
        name="You"
        m = "%s %s" % (name, message)
        G.console.add_message(m, color=color)
        
    def describe(self):
        return "you"
        
    def die(self):
        self.emote("die.", color=colors.dark_red)
        self.is_alive = False
        
                

    