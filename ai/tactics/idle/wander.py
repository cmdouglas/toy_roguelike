import logging
import random
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
        #logging.debug('do_tactics start')
        board = game.board
        if not self.destination:
            #logging.debug('no destination, assigning one')
            self.choose_destination(actor, board)
            self.compute_path(actor, board)
            
            #logging.debug('new destination: %s' % (self.destination,))
            #logging.debug('path: %s' % (self.path,))
            
        if actor.tile.pos == self.destination:
            #logging.debug('hit my destination!')
            if not self.should_stop():
                #logging.debug('wandering again :)')
                # let's wander somewhere else
                self.choose_destination(actor, board)
                self.compute_path(actor, board)
                #logging.debug('new destination: %s' %(self.destination,))
                #logging.debug('path: %s' % (self.path,))
                
            else:
                # nah, let's ask the strategy what to do.
                #logging.debug('stop wandering')
                return (tactics.COMPLETE, None)
                
        #try to move:)'):
        move = self.path[0]
        if self.maybe_move(actor, board, move):
            self.path.pop(0)
            #logging.debug('successfully made move; %s' % (move,))
            # reset our wait timer:
            if self.wait == 0:
                self.wait = dice.d(1, self.max_wait)
            return (tactics.CONTINUE, None)
            
        else:
            #logging.debug('path is blocked')
            # wait and see if the blocker clears
            if self.wait > 0:
                #logging.debug('waiting... %s' % self.wait)
                self.wait -= 1
                return (tactics.CONTINUE, None)
            
            else:
                #logging.debug('finding a new path')
                #ok, let's recompute the path, or go somewhere else
                path_found = self.recompute_path(actor, board, ab=True)
                if not path_found:
                    #logging.debug('no path found, going somewhere else')
                    self.choose_destination(actor, board)
                    self.compute_path(actor, board)
                    
                #logging.debug('new_path: %s' % (self.path,))
                    
        return (tactics.CONTINUE, None)

    def should_stop(self):
        return dice.d(1, 3) == 3

    def choose_destination(self, actor, board):
        area = random.choice(board.areas)
        self.destination = random.choice(area.get_empty_points(board))            
        
    def compute_path(self, actor, board):
        path_found = self.path = search.find_path(board, actor.tile.pos, self.destination)
        while not path_found:
            self.choose_destination(actor, board)
            self.recompute_path(actor, false, ab=True)
        
    def recompute_path(self, actor, board, ab=False):
        self.path = search.find_path(board, actor.tile.pos, self.destination, actors_block=ab)
        return self.path
                
        
        