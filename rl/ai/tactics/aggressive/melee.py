from rl.ai import events, primitives
from rl.ai.tactics import tactics
from rl.actions import interact

class MeleeTactics(tactics.Tactics):
    def __init__(self, target):
        self.target = target

    def describe(self):
        return "fighting %s" % self.target.describe()
        
    def do_tactics(self, actor):
        # does my target exist?
        if not self.target:
            #oh well, must be dead.
            raise events.TacticsCompleteEvent()
        
        # is my target in range?
        tx, ty = self.target.tile.pos
        x, y = actor.tile.pos
        if (abs(tx - x) > 1 or abs(ty - y) > 1):
            if primitives.can_see(actor, self.target):
                raise events.TargetOutOfRangeEvent()

            else:
                # our target has disappeared!
                raise events.TargetLostEvent()
            
        #OK GO
        return interact.AttackAction(actor, self.target)
