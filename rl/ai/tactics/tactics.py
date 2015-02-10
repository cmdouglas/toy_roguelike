
from rl.actions import movement
from rl.actions import interact


class PathBlockedException(Exception):
    pass


class Tactics(object):
    def can_make_move(self, actor, world, move):
        """moves the actor to d, if it's a legal move, and returns true, 
        otherwise returns false
        """
        board = world.board
        
        dx, dy = move
        x, y = actor.tile.pos

        new_pos = (x+dx, y+dy)
        
        return not board[new_pos].blocks_movement()

    def smart_move(self, actor, world, path):
        """will make a move if possible, handling any issues, if possible:
         - if a closed door is in the way, will open it if the actor can.
        """
        move = path[0]

        if self.can_make_move(actor, world, move):
            path.pop(0)
            return movement.MovementAction(actor, move)

        else:
            x, y = actor.tile.pos
            dx, dy = move
            board = world.board
            new_pos = (x+dx, y+dy)
            obstacle = board[new_pos].obstacle
            if obstacle and obstacle.is_door and not obstacle.is_open and actor.can_open_doors:
                return interact.OpenAction(actor, obstacle)

            else:
                raise PathBlockedException()

    def describe(self):
        return ""
