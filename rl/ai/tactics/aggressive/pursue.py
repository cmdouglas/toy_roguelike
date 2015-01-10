import logging

from rl import globals as G
from rl.actions import wait
from rl.ai.tactics import tactics
from rl.ai.utils import search
from rl.ai import events
from rl.ai import primitives

class PursueTactics(tactics.Tactics):
    def __init__(self, target):
        self.target = target
        self.target_pos = target.tile.pos
        
    def describe(self):
        return "chasing %s" % self.target.describe()
        
    def do_tactics(self, actor):
        #logging.debug('Pursue tactics: start')
        board = G.world.board
        self.target_pos = self.target.tile.pos
        
        ax, ay = actor.tile.pos
        tx, ty = self.target.tile.pos
        
        if abs(ax-tx) <= 1 and abs(ay-ty) <= 1:
            #logging.debug('Pursue tactics: target in range')
            #we're close enough to attack!
            raise events.TacticsCompleteEvent()
            
        elif not primitives.can_see(actor, self.target):
            #logging.debug('Pursue tactics: target lost')
            raise events.TargetLostEvent()
            
        else:
            #logging.debug('Pursue tactics: finding path to target')
            path = search.find_path(
                board, 
                actor.tile.pos, 
                self.target.tile.pos, 
                actors_block=False,
                doors_block=not actor.can_open_doors,
                max_depth=20
            )
            
            if path:
                #logging.debug('Pursue tactics: path found')
                try:
                    #logging.debug('Pursue tactics: trying to move')
                    return self.smart_move(actor, path)
                except tactics.PathBlockedException:
                    #logging.debug('Pursue tactics: path blocked')
                    return wait.WaitAction(actor)
                
            else:
                #logging.debug('Pursue tactics: no path found')
                return wait.WaitAction(actor)

            