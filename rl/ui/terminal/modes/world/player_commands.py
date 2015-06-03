
from rl.actions import interact
from rl.actions import movement
from rl.actions import wait
from rl.actions import item

class PlayerCommand:
    """A command given to the player"""
    def __init__(self, world):
        self.world = world


# game mode commands
class WaitCommand(PlayerCommand):
    def process(self, player):
        return wait.WaitAction(player)


class MoveOrInteractCommand(PlayerCommand):
    def __init__(self, world, d):
        super().__init__(world)
        self.d = d

    def process(self, player):
        board = self.world.board
        x, y = player.tile.pos
        dx, dy = self.d
        new_pos = (x+dx, y+dy)

        if (board.position_is_valid(new_pos)
           and board[new_pos].blocks_movement()):

            if board[new_pos].actor:
                other = board[new_pos].actor
                return interact.AttackAction(player, other)

            if board[new_pos].obstacle:
                ob = board[new_pos].obstacle
                return ob.default_interaction(player)

        else:
            return movement.MovementAction(player, self.d)


class DirectionalTravelCommand(PlayerCommand):
    def __init__(self, world, direction, last_surroundings=None):
        super().__init__(world)
        self.direction = direction
        self.last_surroundings = last_surroundings

    def process(self, player):
        first_move = self.last_surroundings is None

        if first_move or not self.should_stop_travelling():
            self.world.player.intelligence.add_command(
                DirectionalTravelCommand(self.world, self.direction, self.get_surroundings())
            )
            return movement.MovementAction(player, self.direction)



    def should_stop_travelling(self):
        # first check if movement is possible:
        player = self.world.player
        cx, cy = self.world.player.tile.pos
        dx, dy = self.direction
        new_pos = (cx+dx, cy+dy)

        if not self.world.board.position_is_valid(new_pos):
            return True

        if self.world.board[new_pos].blocks_movement():
            return True

        # next check for any visible hostiles:
        visible_hostiles = [hostile for hostile in self.world.board.actors
                        if hostile != player and player.can_see(hostile.tile.pos)]


        if visible_hostiles:
            return True

        # if the player is standing on an item, stop
        if player.tile.items:
            return True

        # next check if we've hit a fork in the road
        if self.surroundings_have_changed_meaningfully(self.last_surroundings, self.get_surroundings()):
            return True

        return False


    def get_surroundings(self):
        """grabs a snapshot of what our immediate surroundings look like."""
        s = self.world.player.tile.surrounding(as_dict=True)

        return {
            (-1, -1): self.main_feature(s['nw']),
            (-1, 0): self.main_feature(s['w']),
            (-1, 1): self.main_feature(s['sw']),
            (0, 1): self.main_feature(s['s']),
            (1, 1): self.main_feature(s['se']),
            (1, 0): self.main_feature(s['e']),
            (1, -1): self.main_feature(s['ne']),
            (0, -1): self.main_feature(s['n'])
        }

    def surroundings_have_changed_meaningfully(self, last_surroundings, current_surroundings):
        if not last_surroundings:
            return False
        new = self.new_surrounding_dirs()

        for d in new:
            if last_surroundings[d] != current_surroundings[d]:
                return True

        return False

    def new_surrounding_dirs(self):
        def _horizontal_directions(d):
            return [(d, -1), (d, 0), (d, 1)]

        def _vertical_directions(d):
            return[(-1, d), (0, d), (1, d)]

        dx, dy = self.direction
        s = []
        if dx:
            s.extend(_horizontal_directions(dx))

        if dy:
            s.extend(_vertical_directions(dy))

        return list(set(s))

    def main_feature(self, tile):
        if not tile.obstacle:
            return ' '

        if tile.obstacle.is_wall:
            return '#'

        if tile.obstacle.is_door:
            return '+'

class GetAllItemsCommand(PlayerCommand):
    def process(self, player):
        items = player.tile.items

        if not items:
            return

        for item_ in items:
            player.intelligence.add_command(GetItemCommand(self.world, item_))


class GetItemCommand(PlayerCommand):
    def __init__(self, world, item):
        super().__init__(world)
        self.item = item

    def process(self, player):
        return item.GetItemAction(player, self.item)


class UseItemCommand(PlayerCommand):
    def __init__(self, world, item):
        super().__init__(world)
        self.item = item

    def process(self, player):
        return item.UseItemAction(player, self.item)


class DropItemCommand(PlayerCommand):
    def __init__(self, world, items):
        super().__init__(world)
        self.items = items

    def process(self, player):
        return item.DropItemAction(player, self.items)
