import logging
from actions.wait import WaitAction
from actions.movement import MovementAction
from ai.tactics import tactics
from ai.utils import search
from ai.events.event import TargetLostEvent
from ai import primitives

class PursueTactics(tactics.Tactics):
    def __init__(self, target):
        self.target = target
        self.target_pos = target.tile.pos
        
    def describe(self):
        return "chasing %s" % self.target.describe()
        
    def do_tactics(self, actor, game, events):
        board = game.board
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
            
        elif not primitives.can_see(actor, self.target, board):
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
                if self.can_make_move(actor, board, move):
                    return {
                        'result': tactics.CONTINUE, 
                        'event': None,
                        'action': MovementAction(actor, game, move)
                    }
                else:
                    return {
                        'result': tactics.CONTINUE, 
                        'event': None,
                        'action': WaitAction(actor, game)
                    }
                
            else:
                logging.debug("NO PATH FOUND :(")
                return {
                    'result': tactics.CONTINUE, 
                    'event': None,
                    'action': WaitAction(actor, game)
                }

            