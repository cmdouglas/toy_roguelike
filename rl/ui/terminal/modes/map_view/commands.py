from rl.ui.player_commands import travel
from rl.ai.utils import search

class MapViewCommand:
    def __init__(self, mode):
        self.mode = mode

class MoveCursorCommand(MapViewCommand):
    def __init__(self, mode, dir, repeat=1):
        super().__init__(mode)
        self.dir = dir
        self.repeat = repeat

    def process(self):
        dx, dy = self.dir
        for i in range(self.repeat):
            x, y = self.mode.cursor_pos
            new_pos = (x+dx, y+dy)
            if self.mode.world.board.position_is_valid(new_pos):
                self.mode.cursor_pos = new_pos
                self.mode.changed = True

class GoToPointCommand(MapViewCommand):
    def __init__(self, mode):
        super().__init__(mode)

    def process(self):
        board = self.mode.world.board
        player = self.mode.world.player
        point = self.mode.cursor_pos

        # don't go to the point if we're already there
        if point == player.tile.pos:
            return

        # don't go to the point if there's an obstacle there
        if board[point].obstacle and board[point].blocks_movement:
            return

        # don't go to points that haven't been seen
        if not (board[point].visible or board[point].has_been_seen):
            return

        path = search.find_path(
            board, player.tile.pos, point, doors_block=False, only_known_points=True
        )
        if path:
            player.intelligence.add_command(travel.PathTravelCommand(player, path))
            self.mode.exit()
            return


class JumpToNextInterestingThingCommand(MapViewCommand):
    def process(self):
        if not self.mode.interesting_things:
            return

        ent = self.mode.next_interesting_thing()
        self.mode.cursor_pos = ent.tile.pos
        self.mode.changed = True

class JumpToPreviousInterestingThingCommand(MapViewCommand):
    def process(self):
        if not self.mode.interesting_things:
            return

        ent = self.mode.previous_interesting_thing()
        self.mode.cursor_pos = ent.tile.pos
        self.mode.changed = True

class ExitModeCommand(MapViewCommand):
    def process(self):
        self.mode.exit()