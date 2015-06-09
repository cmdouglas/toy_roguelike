from rl.ui.player_commands import PlayerCommand
from rl.actions import movement


class DirectionalTravelCommand(PlayerCommand):
    def __init__(self, player, direction, last_surroundings=None):
        super().__init__(player)
        self.direction = direction
        self.last_surroundings = last_surroundings

    def process(self):
        first_move = self.last_surroundings is None

        if first_move or not self.should_stop_travelling():
            self.player.intelligence.add_command(
                DirectionalTravelCommand(self.player, self.direction, self.get_surroundings())
            )
            return movement.MovementAction(self.player, self.direction)


    def should_stop_travelling(self):
        # first check if movement is possible:
        cx, cy = self.player.tile.pos
        dx, dy = self.direction
        new_pos = (cx+dx, cy+dy)
        board = self.player.tile.board

        if not board.position_is_valid(new_pos):
            return True

        if board[new_pos].blocks_movement():
            return True

        # next check for any visible hostiles:
        visible_hostiles = [
            hostile for hostile in board.actors
            if hostile != self.player and self.player.can_see_entity(hostile)
        ]

        if visible_hostiles:
            return True

        # if the player is standing on an item, stop
        if self.player.tile.items:
            return True

        # next check if we've hit a fork in the road
        if self.surroundings_have_changed_meaningfully(
                self.last_surroundings,
                self.get_surroundings()):
            return True

        return False


    def get_surroundings(self):
        """grabs a snapshot of what our immediate surroundings look like."""
        s = self.player.tile.neighbors(as_dict=True)

        return {
            d: self.main_feature(s[d])
            for d in s.keys()
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



