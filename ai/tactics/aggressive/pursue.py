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
        
    def describe(self):
        return "chasing %s" % self.target.describe()
        
    def do_tactics(self, actor, game, events):
        board = game.board
        
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
                'event': TargetLostEvent(),
                'action': None
            }
            
        else:
            path = search.find_path(
                board, 
                actor.tile.pos, 
                self.target.tile.pos, 
                actors_block=True
            #    max_depth=20
            )
            
            if path:
                move = path[0]
                return {
                    'result': tactics.CONTINUE, 
                    'event': None,
                    'action': MovementAction(actor, game, move)
                }
                
            else:
                logging.debug("NO PATH FOUND :(")
                return {
                    'result': tactics.CONTINUE, 
                    'event': None,
                    'action': WaitAction(actor, game)
                }

            