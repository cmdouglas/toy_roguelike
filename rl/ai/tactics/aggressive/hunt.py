import logging

from rl import globals as G
from rl.actions.wait import WaitAction
from rl.actions.movement import MovementAction
from rl.ai.tactics import tactics
from rl.ai.utils import search
from rl.ai.events import event
from rl.ai import primitives

class HuntTactics(tactics.Tactics):
    def __init__(self, target):
        self.target = target
        self.pos = target.tile.pos
        
    def describe(self):
        return "hunting %s" % self.target.describe()
        
    def do_tactics(self, actor, events):
        board = G.board
            
        if primitives.can_see(actor, self.target):
            return {
                'result': tactics.INTERRUPTED,
                'event': event.SeeHostileEvent(self.target),
                'action': None
            }
        
        elif actor.tile.pos == self.pos:
            # we've hit where the target was and haven't found him, oh well
            
            return {
                'result': tactics.INTERRUPTED,
                'event': event.InterestLostEvent(),
                'action': WaitAction(actor)
            }
            
        else:
            path = search.find_path(
                board, 
                actor.tile.pos, 
                self.pos, 
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
                
                #there's no way to get to the place the actor was, oh well.
                return {
                    'result': tactics.INTERRUPTED,
                    'event': event.InterestLostEvent(),
                    'action': WaitAction(actor)
                }

            