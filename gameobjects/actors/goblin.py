import random
from io import colors
from gameobjects.actors.mob import Mob
from ai.utils import search
from ai.strategies import idle

class Goblin(Mob):
    def __init__(self):
        self.color = colors.green
        self.char = 'g'
        self.has_seen_player = False
        self.sight_radius = 10
        self.strategy = idle.IdleStrategy()
        self.name="goblin"
        
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
            "scratches its ears.",
            "mutters something unintelligable.",
            "sticks its tongue out at you."
        ])
    
        self.emote(message, game)