import logging
import random
from ai.tactics import tactics
from ai.utils import search
from ai.events import event
from util import dice

class MeleeTactics(tactics.Tactics):
    def __init__(self, target):
        self.target = target

    def describe(self):
        return "fighting you"
        
    def do_tactics(self, actor, game, events):
        # does my target exist?
        if not self.target:
            #oh well, must be dead.
            return (tactics.COMPLETE, None)
        
        # is my target in range?
        tx, ty = self.target.tile.pos
        x, y = actor.pos
        if (abs(tx - x) > 1 or abs(ty - y) > 1):
            return (tactics.INTERRUPTED, events.TargetOutOfRange)    
            
        actor.attack(self.target, game)
        return (tactics.CONTINUE, )
        
        
    def handle_events(self, events):
        pass