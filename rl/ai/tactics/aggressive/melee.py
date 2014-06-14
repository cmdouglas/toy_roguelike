import logging
from rl.ai import events, primitives
from rl.ai.tactics import tactics
from rl.actions import interact

class MeleeTactics(tactics.Tactics):
    def __init__(self, target):
        self.target = target

    def describe(self):
        return "fighting %s" % self.target.describe()
        
    def do_tactics(self, actor):
        #logging.debug('Melee tactics: start')
        # does my target exist?
        if not self.target:
            #logging.debug('Melee tactics: no target')
            #oh well, must be dead.
            raise events.TacticsCompleteEvent()
        
        # is my target in range?
        tx, ty = self.target.tile.pos
        x, y = actor.tile.pos
        if (abs(tx - x) > 1 or abs(ty - y) > 1):
            if primitives.can_see(actor, self.target):
                #logging.debug('Melee tactics: target out of range')
                raise events.TargetOutOfRangeEvent()

            else:
                #logging.debug('Melee tactics: target lost')
                # our target has disappeared!
                raise events.TargetLostEvent()
            
        #OK GO
        #logging.debug('Melee tactics: attacking target')
        return interact.AttackAction(actor, self.target)
