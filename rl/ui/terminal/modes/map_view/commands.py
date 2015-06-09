
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