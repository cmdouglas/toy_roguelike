import logging

from rl import globals as G
from rl.ai import events
from rl.ai.strategies import strategy
from rl.ai.tactics.aggressive import melee, pursue, hunt

logger = logging.getLogger()


class AggressiveStrategy(strategy.Strategy):
    def __init__(self):
        self.target = None
        self.target_last_seen = None
        self.tactics = None

    def do_strategy(self, actor):
        # logger.debug('Aggressive strategy: start')
        if not self.target:
            # logger.debug('Aggressive strategy: finding target')
            self.target = self.nearest_target()

        self.target_last_seen = self.target.tile.pos

        if not self.tactics:
            # logger.debug('Aggressive strategy: setting tactics to pursue')
            self.tactics = pursue.PursueTactics(self.target)

        if type(self.tactics) == melee.MeleeTactics:
            try:
                # logger.debug('Aggressive strategy: doing melee tactics')
                return self.tactics.do_tactics(actor)
            except events.TargetOutOfRangeEvent:
                # logger.debug('Aggressive strategy: target out of range')
                self.target = self.nearest_target()
                if self.target:
                    # logger.debug(
                    #   'Aggressive strategy: setting tactics to pursue'
                    # )
                    self.tactics = pursue.PursueTactics(self.target)

                else:
                    # logger.debug('Aggressive strategy: target lost')
                    raise events.StrategyCompleteEvent()

            except events.TargetLostEvent:
                # logger.debug(
                # 'Aggressive strategy: target lost, setting tactics to hunt'
                # )
                # our target has vanished!
                self.tactics = hunt.HuntTactics(
                    self.target, self.target_last_seen
                )

            except events.TacticsCompleteEvent:
                # logger.debug(
                #   'Aggressive strategy: target gone, strategy complete'
                #  )
                # he's dead, YAY
                raise events.StrategyCompleteEvent()

        elif type(self.tactics == pursue.PursueTactics):
            try:
                # logger.debug('Aggressive strategy: doing pursue tactics')
                return self.tactics.do_tactics(actor)
            except events.TargetLostEvent:
                # logger.debug(
                #    "Aggressive strategy: target lost,"
                #    " setting tactics to hunt"
                # )
                self.tactics = hunt.HuntTactics(
                    self.target, self.target_last_seen
                )

            except events.TacticsCompleteEvent:
                # we're close enough to attack!
                # logger.debug(
                #    'Aggressive strategy: target in range,'
                #    ' setting tactics to melee'
                # )
                self.tactics = melee.MeleeTactics(self.target)

        elif type(self.tactics == hunt.HuntTactics):
            try:
                # logger.debug('Aggressive strategy: doing hunt tactics')
                return self.tactics.do_tactics(actor)
            except events.SeeHostileEvent:
                # logger.debug(
                #     'Aggressive strategy: hostile sighted,'
                #     ' setting tactics to pursue'
                # )
                self.tactics = pursue.PursueTactics(self.target)

            except events.InterestLostEvent:
                # logger.debug(
                #     'Aggressive strategy: unable to find target,'
                #     ' interest lost.'
                # )
                raise

    def nearest_target(self):
        # right now, the only hostile is the player
        return G.world.player

    def describe(self):
        if not self.tactics:
            return 'aggressive'

        return self.tactics.describe()
