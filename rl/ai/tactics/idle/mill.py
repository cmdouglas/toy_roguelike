import random

from rl import globals as G
from rl.ai.tactics.idle import wander
from rl.util import dice

class MillTactics(wander.WanderTactics):
    def __init__(self):
        self.destination = None
        self.path = None
        self.max_wait = 5
        self.wait_timer = self.max_wait
    
    def should_stop(self):
        return dice.one_chance_in(6)
           
    def choose_destination(self, actor):
        area = G.world.board.area_containing_point(actor.tile.pos)
        self.destination = random.choice(area.get_empty_points())
        