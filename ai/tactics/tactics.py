CONTINUE = 0
COMPLETE = 1
INTERRUPTED = 2

class Tactics(object):
    
    def maybe_move(self, actor, board, move):
        """moves the actor to d, if it's a legal move, and returns true, 
        otherwise returns false
        """
        
        dx, dy = move
        x, y = actor.tile.pos
        
        if board[(x+dx, y+dy)].blocks_movement():
            return False
            
        else:
            actor.move((dx, dy))
            return True
            
    def describe(self):
        return ""
