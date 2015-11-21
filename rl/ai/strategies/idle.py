
import random

from rl.ai import events
from rl.ai.strategies import strategy
from rl.ai.tactics.idle import mill, sleep, wander
from rl.save import rl_types

class IdleStrategy(strategy.Strategy):
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

@rl_types.dumper(IdleStrategy, 'idle_strategy', 1)
def _dump_idle_strategy(idle_strategy):
    data = strategy.dump_strategy(idle_strategy)
    return data

@rl_types.loader('idle_strategy', 1)
def _load_idle_strategy(data, version):
    idle_strategy = IdleStrategy()
    strategy.load_strategy(data, idle_strategy)


    return idle_strategy
