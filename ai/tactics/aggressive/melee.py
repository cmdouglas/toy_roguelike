#import logging
from ai.tactics import tactics
from ai.events import event
from actions import attack

class MeleeTactics(tactics.Tactics):
    def __init__(self, target):
        self.target = target

    def describe(self):
        return "fighting %s" % self.target.describe()
        
    def do_tactics(self, actor, game, events):
        # does my target exist?
        if not self.target:
            #oh well, must be dead.
            return {
                'result': tactics.COMPLETE, 
                'event': None,
                'action': None
            }
        
        # is my target in range?
        tx, ty = self.target.tile.pos
        x, y = actor.tile.pos
        if (abs(tx - x) > 1 or abs(ty - y) > 1):
            return {
                'result': tactics.INTERRUPTED, 
                'event': event.TargetOutOfRange(),
                'action': None
            }   
            
        #OK GO
        return {
            'result': tactics.CONTINUE,
            'event': None,
            'action': attack.AttackAction(actor, game, self.target)
        }
        
        
    def handle_events(self, events):
        pass