import random

from rl.ai.tactics.idle import wander
from rl.util import dice

class MillTactics(wander.WanderTactics):
    def __init__(self, strategy):
        super().__init__(strategy)
        self.destination = None
        self.path = None
        self.max_wait = 5
        self.wait_timer = self.max_wait
    
    def should_stop(self):
        return dice.one_chance_in(3)
           
    def choose_destination(self):
        area = self.world.board.area_containing_point(self.actor.tile.pos)
        self.destination = random.choice(area.get_empty_points())
        