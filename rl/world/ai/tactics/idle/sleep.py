from rl.world.ai.tactics import Tactics
from rl.world.ai import primitives, events
from rl.world.actions import wait
from rl.util import dice
#from rl.world.save import rl_types

class SleepTactics(Tactics):
    def __init__(self, strategy=None):
        super().__init__(strategy)
        self.turns_to_sleep = dice.d(2, 50)
        
    def on_start(self, actor):
        pass

    def do_tactics(self):
        if self.actor.can_see_entity(self.world.player):
            raise events.SeeHostileEvent()
        
        self.turns_to_sleep -= 1
        if self.turns_to_sleep == 0:
            raise events.TacticsCompleteEvent()
            
        return wait.WaitAction(self.actor)
            
    def describe(self):
        return "sleeping"


# @rl_types.dumper(SleepTactics, 'sleep_tactics', 1)
# def _dump_sleep_tactics(sleep_tactics):
#     return dict(
#         turns_to_sleep=sleep_tactics.turns_to_sleep,
#     )
#
#
# @rl_types.loader('sleep_tactics', 1)
# def load_sleep_tactics(data, version):
#     sleep_tactics = SleepTactics()
#     sleep_tactics.turns_to_sleep = data['turns_to_sleep']
#
#     return sleep_tactics