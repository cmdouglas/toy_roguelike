import random

from rl.world.ai.tactics.idle import wander
from rl.util import dice
#from rl.world.save import rl_types

class MillTactics(wander.WanderTactics):
    def __init__(self, strategy=None):
        super().__init__(strategy)
        self.destination = None
        self.path = None
        self.max_wait = 5
        self.wait_timer = self.max_wait
    
    def should_stop(self):
        return dice.one_chance_in(3)
           
    def choose_destination(self):
        region = self.world.board.region_containing_point(self.actor.tile.pos)
        self.destination = random.choice(region.empty_points())
