from rl.world.ai.intelligence import Intelligence
from rl.world.ai import events
from rl.world.ai.strategies import idle, aggressive
#from rl.world.save import rl_types


class BasicAI(Intelligence):
        
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

    def restore(self, actors_by_id):
        super().restore(actors_by_id)
        self.strategy.restore(actors_by_id)