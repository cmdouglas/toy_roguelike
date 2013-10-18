
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
        result = self.tactics.do_tactics(actor, game, events)
        
        if result['result'] == tactics.COMPLETE:
            self.tactics = random.choice([
                mill.MillTactics(), 
                sleep.SleepTactics(), 
                wander.WanderTactics()
            ])
            
            result = self.tactics.do_tactics(actor, game, events)
            
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
