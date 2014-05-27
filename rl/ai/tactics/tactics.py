from rl import globals as G

CONTINUE = 0
COMPLETE = 1
INTERRUPTED = 2

class Tactics(object):
    
    def can_make_move(self, actor, move):
        """moves the actor to d, if it's a legal move, and returns true, 
        otherwise returns false
        """
        board = G.board
        
        dx, dy = move
        x, y = actor.tile.pos
        
        return not board[(x+dx, y+dy)].blocks_movement()
            
    def describe(self):
        return ""
