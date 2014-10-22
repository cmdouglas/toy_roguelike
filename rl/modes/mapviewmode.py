from rl import globals as G
from rl.modes import mode
from rl.io import console
from rl.io import colors
from rl.io.terminal.modes.mapview import commands
from rl.io.terminal.modes.mapview import render
from rl.board.generator import generator

class MapViewMode(mode.Mode):
    def __init__(self, start_pos, parent=None, data=None):
        super(MapViewMode, self).__init__(parent=parent, data=data)

        self.pos = start_pos

    def process(self):
        pass

