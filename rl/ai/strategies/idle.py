
import random

from rl.ai import events
from rl.ai.strategies import strategy
from rl.ai.tactics import tactics
from rl.ai.tactics.idle import mill, sleep, wander

class IdleStrategy(strategy.Strategy):
    def __init__(self):
        self.tactics = random.choice([
            mill.MillTactics(), 
            sleep.SleepTactics(), 
            wander.WanderTactics()
        ])
    
    def do_strategy(self, actor):
        try:
            return self.tactics.do_tactics(actor)
        except events.TacticsCompleteEvent:
            self.tactics = random.choice([
                mill.MillTactics(),
                sleep.SleepTactics(),
                wander.WanderTactics()
            ])

        except events.SeeHostileEvent:
            raise

            
    def describe(self):
        return self.tactics.describe()
