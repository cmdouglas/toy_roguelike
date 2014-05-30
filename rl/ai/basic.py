from rl.ai import events
from rl.ai.strategies import idle, aggressive, strategy


class BasicAI(object):
    def __init__(self, actor):
        
        self.actor = actor
        self.strategy = idle.IdleStrategy()
        
    def do_ai(self):
        try:
            return self.strategy.do_strategy(self.actor)

        except events.SeeHostileEvent:
            self.strategy = aggressive.AggressiveStrategy()
        
        except events.InterestLostEvent:
            self.strategy = idle.IdleStrategy()

        except events.StrategyCompleteEvent:
            self.strategy = idle.IdleStrategy()
