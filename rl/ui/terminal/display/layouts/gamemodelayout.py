import logging

from termapp.layout import Layout
from termapp.term import term

from rl.ui.terminal.display.panes import board
from rl.ui.terminal.display.panes import console
from rl.ui.terminal.display.panes import hud

from rl import globals as G

logger = logging.getLogger('rl')


class GameModeLayout(Layout):
    def __init__(self):
        super(GameModeLayout, self).__init__()
        self.refresh()

    def refresh(self):
        console_width = term.width
        console_height = 4

        hud_width = 44
        hud_height = (term.height - console_height) - 1

        viewport_width = min((term.width - (hud_width + 2), 80))
        viewport_height = min(((term.height - console_height) - 1, 80))

        viewport_pos = (0, 0)
        hud_pos = (viewport_width, 0)
        console_pos = (0, viewport_height)

        self.board_pane = board.BoardPane(viewport_width, viewport_height)
        self.hud_pane = hud.HUDPane(hud_width, hud_height)
        self.console_pane = console.ConsolePane(console_width, console_height)

        self.panes = {
            viewport_pos: self.board_pane,
            hud_pos: self.hud_pane,
            console_pos: self.console_pane
        }

    def render(self):
        self.board_pane.center = G.world.player.tile.pos
        return super().render()
