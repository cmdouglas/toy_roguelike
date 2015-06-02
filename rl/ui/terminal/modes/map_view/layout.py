import logging

from termapp.layout import Layout
from termapp.term import term

from rl.ui.terminal.display.panes import board
from rl.ui.terminal.display.panes import console
from rl.ui.terminal.display.panes import hud
from rl.ui.terminal.display.panes import objects_of_interest

logger = logging.getLogger('rl')


class ExamineModeLayout(Layout):
    def __init__(self, world, console):
        super().__init__()
        self.world = world
        self.console = console
        self.refresh()

    def refresh(self):
        console_width = term.width
        console_height = 4

        hud_width = 46
        hud_height = 11

        examined_object_width = 46
        examined_object_height = term.height - console_height - hud_height - 1

        viewport_width = min((term.width - hud_width, 80))
        viewport_height = min(((term.height - console_height) - 1, 80))

        viewport_pos = (0, 0)
        hud_pos = (viewport_width, 0)
        examined_object_pos = (viewport_width, hud_height)
        console_pos = (0, viewport_height)

        self.board_pane = board.BoardPane(viewport_width, viewport_height, self.world)
        self.hud_pane = hud.HUDPane(hud_width, hud_height, self.world)
        self.examined_object_pane = objects_of_interest.ObjectsOfInterestPane(
            examined_object_width, examined_object_height, self.world
        )
        self.console_pane = console.ConsolePane(console_width, console_height, self.console)

        self.panes = {
            viewport_pos: self.board_pane,
            hud_pos: self.hud_pane,
            examined_object_pos: self.examined_object_pane,
            console_pos: self.console_pane
        }

    def render(self):
        self.board_pane.center = self.world.player.tile.pos
        return super().render()
