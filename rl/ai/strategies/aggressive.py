import logging

from rl.ai import events
from rl.ai.strategies import strategy
from rl.ai.tactics.aggressive import melee, pursue, hunt
from rl.save import rl_types

logger = logging.getLogger()


class AggressiveStrategy(strategy.Strategy):
    def __init__(self, intelligence):
        super().__init__(intelligence)
        self.target = None
        self.target_last_seen = None

    def do_strategy(self):
        # logger.debug('Aggressive strategy: start')
        if not self.target:
            # logger.debug('Aggressive strategy: finding target')
            self.target = self.nearest_target()

        self.target_last_seen = self.target.tile.pos

        if not self.tactics:
            # logger.debug('Aggressive strategy: setting tactics to pursue')
            self.tactics = pursue.PursueTactics(self)

        if type(self.tactics) == melee.MeleeTactics:
            try:
                # logger.debug('Aggressive strategy: doing melee tactics')
                return self.tactics.do_tactics()
            except events.TargetOutOfRangeEvent:
                # logger.debug('Aggressive strategy: target out of range')
                self.target = self.nearest_target()
                if self.target:
                    # logger.debug(
                    #   'Aggressive strategy: setting tactics to pursue'
                    # )
                    self.tactics = pursue.PursueTactics(self)

                else:
                    # logger.debug('Aggressive strategy: target lost')
                    raise events.StrategyCompleteEvent()

            except events.TargetLostEvent:
                # logger.debug(
                # 'Aggressive strategy: target lost, setting tactics to hunt'
                # )
                # our target has vanished!
                self.tactics = hunt.HuntTactics(self)

            except events.TacticsCompleteEvent:
                # logger.debug(
                #   'Aggressive strategy: target gone, strategy complete'
                #  )
                # he's dead, YAY
                raise events.StrategyCompleteEvent()

        elif type(self.tactics == pursue.PursueTactics):
            try:
                # logger.debug('Aggressive strategy: doing pursue tactics')
                return self.tactics.do_tactics()
            except events.TargetLostEvent:
                # logger.debug(
                #    "Aggressive strategy: target lost,"
                #    " setting tactics to hunt"
                # )
                self.tactics = hunt.HuntTactics(self)

            except events.TacticsCompleteEvent:
                # we're close enough to attack!
                # logger.debug(
                #    'Aggressive strategy: target in range,'
                #    ' setting tactics to melee'
                # )
                self.tactics = melee.MeleeTactics(self)

        elif type(self.tactics == hunt.HuntTactics):
            try:
                # logger.debug('Aggressive strategy: doing hunt tactics')
                return self.tactics.do_tactics()
            except events.SeeHostileEvent:
                # logger.debug(
                #     'Aggressive strategy: hostile sighted,'
                #     ' setting tactics to pursue'
                # )
                self.tactics = pursue.PursueTactics(self)

            except events.InterestLostEvent:
                # logger.debug(
                #     'Aggressive strategy: unable to find target,'
                #     ' interest lost.'
                # )
                raise

    def nearest_target(self):
        # right now, the only hostile is the player
        return self.world.player

    def describe(self):
        if not self.tactics:
            return 'aggressive'

        return self.tactics.describe()

@rl_types.dumper(AggressiveStrategy, 'aggressive_strategy', 1)
def _dump_aggressive_strategy(aggressive_strategy):
    data = strategy.dump_strategy(aggressive_strategy)
    data.update(dict(
        target=id(aggressive_strategy.target),
        target_last_seen=aggressive_strategy.target_last_seen
    ))
    return data

@rl_types.loader('aggressive_strategy', 1)
def _load_aggressive_strategy(data, version):
    aggressive_strategy = AggressiveStrategy()
    strategy.load_strategy(data, aggressive_strategy)
    aggressive_strategy.saved_target = data['target']
    aggressive_strategy.target_last_seen = data['target_last_seen']

    return aggressive_strategy
