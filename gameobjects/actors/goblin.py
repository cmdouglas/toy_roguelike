import random
from gameio import colors
from gameobjects.actors.mob import Mob
from ai.utils import search
from ai.strategies import idle

class Goblin(Mob):
    name="goblin"
    name_plural = "goblins"
    interest_level = 10
    color = colors.green
    char = 'g'
    sight_radius = 8 
    
    def __init__(self):
        self.strategy = idle.IdleStrategy()
        
    def process_turn(self, game):
        self.strategy.do_strategy(self, game, [])
        return True

    def sleep_emote(self, game):
        message = random.choice([
            "snores.",
            "mumbles something in its sleep."
        ])
        
        self.emote(message, game)
        
    def idle_emote(self, game):
        message = random.choice([
            "snorts.",
            "blinks dimly at you.",
            "scratches its ears.",
            "mutters something unintelligable.",
            "sticks its tongue out at you."
        ])
    
        self.emote(message, game)