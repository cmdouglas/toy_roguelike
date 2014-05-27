import logging

from rl import globals as G
from rl.actions.wait import WaitAction
from rl.actions.movement import MovementAction
from rl.ai.tactics import tactics
from rl.ai.utils import search
from rl.ai.events.event import TargetLostEvent
from rl.ai import primitives

class PursueTactics(tactics.Tactics):
    def __init__(self, target):
        self.target = target
        self.target_pos = target.tile.pos
        
    def describe(self):
        return "chasing %s" % self.target.describe()
        
    def do_tactics(self, actor, events):
        board = G.board
        self.target_pos = self.target.tile.pos
        
        ax, ay = actor.tile.pos
        tx, ty = self.target.tile.pos
        
        if abs(ax-tx) <= 1 and abs(ay-ty) <= 1:
            #we're close enough to attack!
            return {
                'result': tactics.COMPLETE,
                'event': None,
                'action': None
            }
            
        elif not primitives.can_see(actor, self.target):
            return {
                'result': tactics.INTERRUPTED,
                'event': TargetLostEvent(self.target_pos),
                'action': None
            }
            
        else:
            path = search.find_path(
                board, 
                actor.tile.pos, 
                self.target.tile.pos, 
                actors_block=False,
                max_depth=20
            )
            
            if path:
                move = path[0]
                if self.can_make_move(actor, move):
                    return {
                        'result': tactics.CONTINUE, 
                        'event': None,
                        'action': MovementAction(actor, move)
                    }
                else:
                    return {
                        'result': tactics.CONTINUE, 
                        'event': None,
                        'action': WaitAction(actor)
                    }
                
            else:
                return {
                    'result': tactics.CONTINUE, 
                    'event': None,
                    'action': WaitAction(actor)
                }

            