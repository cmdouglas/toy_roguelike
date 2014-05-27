
import random

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
    
    def do_strategy(self, actor, events):
        result = self.tactics.do_tactics(actor, events)
        
        if result['result'] == tactics.COMPLETE:
            self.tactics = random.choice([
                mill.MillTactics(), 
                sleep.SleepTactics(), 
                wander.WanderTactics()
            ])
            
            result = self.tactics.do_tactics(actor, events)
            
            return {
                'result': strategy.CONTINUE,
                'event': None,
                'action': result['action']
            }
            
        elif result['result'] == tactics.INTERRUPTED:
            return {
                'result': strategy.INTERRUPTED,
                'event': result['event'],
                'action': result['action']
            }
            
        else:
            return {
                'result': strategy.CONTINUE,
                'event': None,
                'action': result['action']
            }
            
    def describe(self):
        return self.tactics.describe()
