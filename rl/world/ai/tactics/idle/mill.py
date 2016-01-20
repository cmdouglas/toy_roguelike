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

# @rl_types.dumper(MillTactics, 'mill_tactics', 1)
# def _dump_mill_tactics(mill_tactics):
#     return dict(
#         destination=mill_tactics.destination,
#         path=mill_tactics.path,
#         max_wait=mill_tactics.max_wait,
#         wait_timer=mill_tactics.wait_timer
#     )
#
#
# @rl_types.loader('mill_tactics', 1)
# def load_mill_tactics(data, version):
#     mill_tactics = MillTactics()
#     mill_tactics.destination = data['destination']
#     mill_tactics.path = data['path']
#     mill_tactics.max_wait = data['max_wait']
#     mill_tactics.wait_timer = data['wait_timer']
#
#     return mill_tactics