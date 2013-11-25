import logging
from actions.wait import WaitAction
from actions.movement import MovementAction
from ai.tactics import tactics
from ai.utils import search
from ai.events import event
from ai import primitives

class HuntTactics(tactics.Tactics):
    def __init__(self, target):
        self.target = target
        self.pos = target.tile.pos
        
    def describe(self):
        return "hunting %s" % self.target.describe()
        
    def do_tactics(self, actor, game, events):
        board = game.board
        
        ax, ay = actor.tile.pos
        tx, ty = self.target.tile.pos
            
        if primitives.can_see(actor, self.target, board):
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
                'action': WaitAction(actor, game)
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
                
                #there's no way to get to the place the actor was, oh well.
                return {
                    'result': tactics.INTERRUPTED,
                    'event': event.InterestLostEvent(),
                    'action': WaitAction(actor, game)
                }

            