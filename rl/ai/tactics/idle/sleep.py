from rl.ai.tactics import Tactics
from rl.ai import primitives, events
from rl.actions import wait
from rl.util import dice

class SleepTactics(Tactics):
    def __init__(self, strategy):
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
        