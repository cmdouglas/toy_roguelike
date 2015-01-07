from rl import globals as G
from rl.modes import mode
from rl.ui import console
from rl.ui import colors
from rl.ui.terminal.modes.mapview import commands
from rl.ui.terminal.modes.mapview import render
from rl.board.generator import generator

class MapViewMode(mode.Mode):
    def __init__(self, start_pos, parent=None, data=None):
        super(MapViewMode, self).__init__(parent=parent, data=data)

        self.pos = start_pos

    def process(self):
        pass

