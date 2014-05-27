import random
from rl.io import colors
from rl.objects.actors.mob import Mob
from rl.ai.basic import BasicAI

class Goblin(Mob):
    name=u"goblin"
    name_plural = u"goblins"
    interest_level = 10
    color = colors.green
    char = u'g'
    sight_radius = 8 
    max_health = 10
    
    def __init__(self):
        self.health = self.max_health
        self.ai = BasicAI(self)
        self.str = 4
        
    def process_turn(self):
        
        action = self.ai.do_ai()
        action.do_action()
        return True

    def sleep_emote(self):
        message = random.choice([
            "snores.",
            "mumbles something in its sleep."
        ])
        
        self.emote(message)
        
    def idle_emote(self):
        message = random.choice([
            "growls.",
            "blinks dimly.",
            "scratches its ears.",
            "mutters something unintelligable.",
            "sticks its tongue out."
        ])
    
        self.emote(message)