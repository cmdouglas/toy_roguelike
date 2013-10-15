
import random
from ai.strategies import strategy
from ai.tactics import tactics
from ai.tactics.idle import mill, sleep, wander

class IdleStrategy(strategy.Strategy):
    def __init__(self):
        self.tactics = random.choice([
            mill.MillTactics(), 
            sleep.SleepTactics(), 
            wander.WanderTactics()
        ])
    
    def do_strategy(self, actor, game, events):
        result, event = self.tactics.do_tactics(actor, game, events)
        
        if result == tactics.COMPLETE:
            self.tactics = random.choice([
                mill.MillTactics(), 
                sleep.SleepTactics(), 
                wander.WanderTactics()
            ])
            
            return (strategy.CONTINUE, None)
            
        elif result == tactics.INTERRUPTED:
            return (strategy.INTERRUPTED, event)
            
        else:
            return (strategy.CONTINUE, None)
            
    def describe(self):
        return self.tactics.describe()
