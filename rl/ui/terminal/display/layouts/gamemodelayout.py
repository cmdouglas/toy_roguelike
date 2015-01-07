from termapp.layout import Layout
from termapp.term import term

from rl.ui.terminal.display.panes import board
from rl.ui.terminal.display.panes import console
from rl.ui.terminal.display.panes import hud

class GameModeLayout(Layout):
    def __init__(self):
        super(GameModeLayout, self).__init__()

        console_width = term.width
        console_height = 5

        hud_width = 44
        hud_height = term.height - console_height

        viewport_width = term.width - (hud_width + 2)
        viewport_height = term.height - console_height

        viewport_pos = (0, 0)
        hud_pos = (viewport_width, 0)
        console_pos = (0, viewport_height)

        self.panes = {
            viewport_pos: board.BoardPane(viewport_width, viewport_height),
            hud_pos: hud.HUDPane(hud_width, hud_height),
            console_pos: console.ConsolePane(console_width, console_height)
        }
