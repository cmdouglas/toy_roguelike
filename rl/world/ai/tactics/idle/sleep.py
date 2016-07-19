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
        if self.actor.can_see_entity(self.actor.tile.board.world.player) and dice.one_chance_in(6):
            raise events.SeeHostileEvent()
        
        self.turns_to_sleep -= 1
        if self.turns_to_sleep == 0:
            raise events.TacticsCompleteEvent()
            
        return wait.WaitAction(self.actor)
            
    def describe(self):
        return "sleeping"

    def __getstate__(self):
        return dict(
            turns_to_sleep=self.turns_to_sleep
        )

    def __setstate__(self, state):
        self.turns_to_sleep = state['turns_to_sleep']
