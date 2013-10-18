CONTINUE = 0
COMPLETE = 1
INTERRUPTED = 2

class Tactics(object):
    
    def can_make_move(self, actor, board, move):
        """moves the actor to d, if it's a legal move, and returns true, 
        otherwise returns false
        """
        
        dx, dy = move
        x, y = actor.tile.pos
        
        if board[(x+dx, y+dy)].blocks_movement():
            return False
            
        else:
            return True
            
    def describe(self):
        return ""
