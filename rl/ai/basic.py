from rl.ai import intelligence
from rl.ai import events
from rl.ai.strategies import idle, aggressive


class BasicAI(intelligence.Intelligence):
        
    def get_action(self):
        if not self.strategy:
            self.strategy = idle.IdleStrategy(self)

        try:
            return self.strategy.do_strategy()

        except events.SeeHostileEvent:
            self.strategy = aggressive.AggressiveStrategy(self)
        
        except events.InterestLostEvent:
            self.strategy = idle.IdleStrategy(self)

        except events.StrategyCompleteEvent:
            self.strategy = idle.IdleStrategy(self)
