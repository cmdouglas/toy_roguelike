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
        if not self.target:
            self.target = self.nearest_target()

        self.target_last_seen = self.target.tile.pos

        if not self.tactics:
            self.tactics = pursue.PursueTactics(self.target)
            
        if type(self.tactics) == melee.MeleeTactics:
            try:
                return self.tactics.do_tactics(actor)
            except events.TargetOutOfRangeEvent:
                self.target = self.nearest_target()
                if self.target:
                    self.tactics = pursue.PursueTactics(self.target)

                else:
                    raise events.StrategyCompleteEvent()

            except events.TargetLostEvent:
                # our target has vanished!
                self.tactics = hunt.HuntTactics(self.target, self.target_last_seen)

            except events.TacticsCompleteEvent:
                # he's dead, YAY
                raise events.StrategyCompleteEvent()


        elif type(self.tactics == pursue.PursueTactics):
            try:
                return self.tactics.do_tactics(actor)
            except events.TargetLostEvent:
                self.tactics = hunt.HuntTactics(self.target, self.target_last_seen)

            except events.TacticsCompleteEvent:
                #we're close enough to attack!
                self.tactics = melee.MeleeTactics(self.target)

        elif type(self.tactics == hunt.HuntTactics):
            try:
                return self.tactics.do_tactics(actor)
            except events.SeeHostileEvent:
                self.tactics = pursue.PursueTactics(self.target)

            except events.InterestLostEvent:
                raise
        
    def nearest_target(self):
        # right now, the only hostile is the player
        return G.player
    
    def describe(self):
        if not self.tactics:
            return 'aggressive'
            
        return self.tactics.describe()