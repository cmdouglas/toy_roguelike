import random
from actions.wait import WaitAction
from actions.movement import MovementAction
from ai.tactics import tactics
from ai.utils import search
from util import dice

class WanderTactics(tactics.Tactics):
    def __init__(self):
        self.destination = None
        self.path = None
        self.max_wait = 5
        self.wait = random.randrange(self.max_wait) + 1
        
    def do_tactics(self, actor, game, events):
        board = game.board
        
        if dice.one_chance_in(10):
            actor.idle_emote(game)
        
        if not self.destination:
            self.choose_destination(actor, board)
            self.compute_path(actor, board)
            
        if actor.tile.pos == self.destination:
            if not self.should_stop():
                # let's wander somewhere else
                self.choose_destination(actor, board)
                self.compute_path(actor, board)
                
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
                'action': WaitAction(actor, game)
            }
        
        move = self.path[0]
        if self.can_make_move(actor, board, move):
            self.path.pop(0)
            # reset our wait timer:
            if self.wait == 0:
                self.wait = dice.d(1, self.max_wait)
            return {
                'result': tactics.CONTINUE, 
                'event': None,
                'action': MovementAction(actor, game, move)
            }
            
        else:
            # wait and see if the blocker clears
            if self.wait > 0:
                self.wait -= 1
                return {
                    'result': tactics.CONTINUE, 
                    'event': None,
                    'action': WaitAction(actor, game)
                }
            
            else:
                #ok, let's recompute the path, or go somewhere else
                path_found = self.recompute_path(actor, board, ab=True, md=10)
                if not path_found:
                    #logging.debug('no path found, going somewhere else')
                    dest = self.nearby_reachable_destination(actor, board)
                    if dest:
                        self.destination = dest
                        self.compute_path(actor, board)
                                        
        return {
            'result': tactics.CONTINUE, 
            'event': None,
            'action': WaitAction(actor, game)
        }

    def should_stop(self):
        return dice.d(1, 3) == 3

    def nearby_reachable_destination(self, actor, board):
        p = actor.tile.pos
        points = board.nearby_reachable_points(p, 5)
        if points:
            return random.choice(points)

    def choose_destination(self, actor, board):
        actors_area = board.area_containing_point(actor.tile.pos)
        area = random.choice(actors_area.connections)['area']
        self.destination = random.choice(area.get_empty_points(board))            
        
    def compute_path(self, actor, board):
        path_found = self.path = search.find_path(board, actor.tile.pos, self.destination, actors_block=False)
        if not path_found:
            dest = self.nearby_reachable_destination(actor, board)
            if dest:
                self.destination = dest
                self.recompute_path(actor, board, ab=True)
        
    def recompute_path(self, actor, board, ab=False, md=None):
        self.path = search.find_path(board, actor.tile.pos, self.destination, actors_block=ab, max_depth=md)
        return self.path
        
        
    def describe(self):
        return "wandering"
                
        
        