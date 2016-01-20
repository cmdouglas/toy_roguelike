from rl.world.ai.intelligence import Intelligence, dump_intelligence, load_intelligence
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


# @rl_types.dumper(BasicAI, 'basic_ai', 1)
# def _dump_basic_ai(basic_ai):
#     return dump_intelligence(basic_ai)
#
#
# @rl_types.loader('basic_ai', 1)
# def _load_basic_ai(data, version):
#     basic_ai = BasicAI()
#     load_intelligence(data, basic_ai)
#
#     return basic_ai