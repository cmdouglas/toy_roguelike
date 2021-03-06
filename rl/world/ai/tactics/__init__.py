
from rl.world.actions import movement
from rl.world.actions import interact


class PathBlockedException(Exception):
    pass


class Tactics(object):
    def __init__(self, strategy=None):
        self.strategy = strategy

    @property
    def actor(self):
        return self.strategy.intelligence.actor

    @property
    def board(self):
        return self.actor.tile.board

    @property
    def world(self):
        return self.board.world

    def can_make_move(self, move):
        """moves the actor to d, if it's a legal move, and returns true,
        otherwise returns false
        """

        dx, dy = move
        x, y = self.actor.tile.pos

        new_pos = (x+dx, y+dy)

        return not self.board[new_pos].blocks_movement()

    def smart_move(self, path):
        """will make a move if possible, handling any issues, if possible:
         - if a closed door is in the way, will open it if the actor can.
        """
        move = path[0]

        if self.can_make_move(move):
            path.pop(0)
            return movement.MovementAction(self.actor, move)

        else:
            x, y = self.actor.tile.pos
            dx, dy = move
            board = self.world.board
            new_pos = (x+dx, y+dy)
            terrain = board[new_pos].terrain
            if terrain.blocks_movement and terrain.is_door and self.actor.can_open_doors:
                return interact.OpenAction(self.actor, terrain)

            else:
                raise PathBlockedException()

    def describe(self):
        return ""

    def __getstate__(self):
        return {}
