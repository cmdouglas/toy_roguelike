from rl.ai.strategies import idle, aggressive, strategy
from rl.ai.events import event

class BasicAI(object):
    def __init__(self, actor):
        
        self.actor = actor
        self.strategy = idle.IdleStrategy()
        
    def do_ai(self):        
        r = self.strategy.do_strategy(self.actor, [])
        
        if r['result'] == strategy.INTERRUPTED:
            if type(r['event']) == event.SeeHostileEvent:
                self.strategy = aggressive.AggressiveStrategy() 
                
            else:
                self.strategy = idle.IdleStrategy()
        
        return r['action']