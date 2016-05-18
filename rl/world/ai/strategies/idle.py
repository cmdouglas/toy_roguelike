
import random

from rl.world.ai import events
from rl.world.ai.strategies import Strategy
from rl.world.ai.tactics.idle import mill, sleep, wander

class IdleStrategy(Strategy):
    def __init__(self, intelligence=None):
        super().__init__(intelligence)
        self.tactics = random.choice([
            mill.MillTactics(self),
            sleep.SleepTactics(self),
            wander.WanderTactics(self)
        ])
    
    def do_strategy(self):
        try:
            return self.tactics.do_tactics()
        except events.TacticsCompleteEvent:
            self.tactics = random.choice([
                mill.MillTactics(self),
                sleep.SleepTactics(self),
                wander.WanderTactics(self)
            ])

        except events.SeeHostileEvent:
            raise

            
    def describe(self):
        return self.tactics.describe()
