from rl.world.actions import interact
from rl.world.actions import movement
from rl.world.actions import wait


class PlayerCommand:
    """A command given to the player"""
    def __init__(self, player):
        self.player = player

class WaitCommand(PlayerCommand):
    def process(self):
        return wait.WaitAction(self.player)


class MoveOrInteractCommand(PlayerCommand):
    def __init__(self, player, d):
        super().__init__(player)
        self.d = d

    def process(self):
        board = self.player.tile.board
        x, y = self.player.tile.pos
        dx, dy = self.d
        new_pos = (x+dx, y+dy)

        if (board.position_is_valid(new_pos)
           and board[new_pos].blocks_movement()):

            if board[new_pos].creature:
                other = board[new_pos].creature
                return interact.AttackAction(self.player, other)

            if board[new_pos].terrain:
                ob = board[new_pos].terrain
                return ob.default_interaction(self.player)

        else:
            return movement.MovementAction(self.player, self.d)