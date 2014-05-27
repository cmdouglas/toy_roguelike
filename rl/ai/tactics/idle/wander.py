import random

from rl import globals as G
from rl.actions.wait import WaitAction
from rl.actions.movement import MovementAction
from rl.ai import primitives
from rl.ai.events import event
from rl.ai.tactics import tactics
from rl.ai.utils import search
from rl.util import dice

class WanderTactics(tactics.Tactics):
    def __init__(self):
        self.destination = None
        self.path = None
        self.max_wait = 5
        self.wait = random.randrange(self.max_wait) + 1
        
    def do_tactics(self, actor, events):
        board = G.board
        
        if (primitives.can_see(actor, G.player) and dice.one_chance_in(2)):
            actor.emote('points at you and shouts!')
            return {
                'result': tactics.INTERRUPTED,
                'event': event.SeeHostileEvent(),
                'action': WaitAction(actor)
            }
        
        if dice.one_chance_in(10):
            actor.idle_emote()
        
        if not self.destination:
            self.choose_destination(actor)
            self.compute_path(actor)
            
        if actor.tile.pos == self.destination:
            if not self.should_stop():
                # let's wander somewhere else
                self.choose_destination(actor)
                self.compute_path(actor)
                
            else:
                # nah, let's ask the strategy what to do.
                return {
                    'result': tactics.COMPLETE, 
                    'event': None,
                    'action': None    
                }
                
        #try to move:
        if not self.path:
            self.destination = None
            return {
                'result': tactics.CONTINUE, 
                'event': None,
                'action': WaitAction(actor)
            }
        
        move = self.path[0]
        if self.can_make_move(actor, move):
            self.path.pop(0)
            # reset our wait timer:
            if self.wait == 0:
                self.wait = dice.d(1, self.max_wait)
            return {
                'result': tactics.CONTINUE, 
                'event': None,
                'action': MovementAction(actor, move)
            }
            
        else:
            # wait and see if the blocker clears
            if self.wait > 0:
                self.wait -= 1
                return {
                    'result': tactics.CONTINUE, 
                    'event': None,
                    'action': WaitAction(actor)
                }
            
            else:
                #ok, let's recompute the path, or go somewhere else
                path_found = self.recompute_path(actor, ab=True, md=10)
                if not path_found:
                    #logging.debug('no path found, going somewhere else')
                    dest = self.nearby_reachable_destination(actor)
                    if dest:
                        self.destination = dest
                        self.compute_path(actor)
                                        
        return {
            'result': tactics.CONTINUE, 
            'event': None,
            'action': WaitAction(actor)
        }

    def should_stop(self):
        return dice.d(1, 3) == 3

    def nearby_reachable_destination(self, actor):
        board = G.board
        p = actor.tile.pos
        points = board.nearby_reachable_points(p, 5)
        if points:
            return random.choice(points)

    def choose_destination(self, actor):
        board = G.board
        actors_area = board.area_containing_point(actor.tile.pos)
        area = random.choice(actors_area.connections)['area']
        self.destination = random.choice(area.get_empty_points())
        
    def compute_path(self, actor):
        board = G.board
        path_found = self.path = search.find_path(board, actor.tile.pos, self.destination, actors_block=False)
        if not path_found:
            dest = self.nearby_reachable_destination(actor)
            if dest:
                self.destination = dest
                self.recompute_path(actor, ab=True)
        
    def recompute_path(self, actor, ab=False, md=None):
        board = G.board
        self.path = search.find_path(board, actor.tile.pos, self.destination, actors_block=ab, max_depth=md)
        return self.path
        
        
    def describe(self):
        return "wandering"
                
        
        