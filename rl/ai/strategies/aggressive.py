import logging

from rl import globals as G
from rl import ai
from rl.ai import events
from rl.ai.strategies import strategy
from rl.ai.tactics import tactics
from rl.ai.tactics.aggressive import melee, pursue, hunt
from rl.actions import wait

class AggressiveStrategy(strategy.Strategy):
    def __init__(self):
        self.target = None
        self.target_last_seen = None
        self.tactics = None
    
    def do_strategy(self, actor):
        #logging.debug('Aggressive strategy: start')
        if not self.target:
            #logging.debug('Aggressive strategy: finding target')
            self.target = self.nearest_target()

        self.target_last_seen = self.target.tile.pos

        if not self.tactics:
            #logging.debug('Aggressive strategy: setting tactics to pursue')
            self.tactics = pursue.PursueTactics(self.target)
            
        if type(self.tactics) == melee.MeleeTactics:
            try:
                #logging.debug('Aggressive strategy: doing melee tactics')
                return self.tactics.do_tactics(actor)
            except events.TargetOutOfRangeEvent:
                #logging.debug('Aggressive strategy: target out of range')
                self.target = self.nearest_target()
                if self.target:
                    #logging.debug('Aggressive strategy: setting tactics to pursue')
                    self.tactics = pursue.PursueTactics(self.target)

                else:
                    #logging.debug('Aggressive strategy: target lost')
                    raise events.StrategyCompleteEvent()

            except events.TargetLostEvent:
                #logging.debug('Aggressive strategy: target lost, setting tactics to hunt')
                # our target has vanished!
                self.tactics = hunt.HuntTactics(self.target, self.target_last_seen)

            except events.TacticsCompleteEvent:
                #logging.debug('Aggressive strategy: target gone, strategy complete')
                # he's dead, YAY
                raise events.StrategyCompleteEvent()


        elif type(self.tactics == pursue.PursueTactics):
            try:
                #logging.debug('Aggressive strategy: doing pursue tactics')
                return self.tactics.do_tactics(actor)
            except events.TargetLostEvent:
                #logging.debug('Aggressive strategy: target lost, setting tactics to hunt')
                self.tactics = hunt.HuntTactics(self.target, self.target_last_seen)

            except events.TacticsCompleteEvent:
                #we're close enough to attack!
                #logging.debug('Aggressive strategy: target in range, setting tactics to melee')
                self.tactics = melee.MeleeTactics(self.target)

        elif type(self.tactics == hunt.HuntTactics):
            try:
                #logging.debug('Aggressive strategy: doing hunt tactics')
                return self.tactics.do_tactics(actor)
            except events.SeeHostileEvent:
                #logging.debug('Aggressive strategy: hostile sighted, setting tactics to pursue')
                self.tactics = pursue.PursueTactics(self.target)

            except events.InterestLostEvent:
                #logging.debug('Aggressive strategy: unable to find target, interest lost.')
                raise
        
    def nearest_target(self):
        # right now, the only hostile is the player
        return G.player
    
    def describe(self):
        if not self.tactics:
            return 'aggressive'
            
        return self.tactics.describe()