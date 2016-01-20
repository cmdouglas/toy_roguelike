import logging

from termapp.layout import Layout
from termapp.term import term

from rl.ui.terminal.display.panes import board
from rl.ui.terminal.display.panes import log
from rl.ui.terminal.display.panes import hud
from rl.ui.terminal.display.panes import examined_object
from rl.ui import colors

logger = logging.getLogger('rl')


class ExamineModeLayout(Layout):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode

        log_width = term.width
        log_height = 4

        hud_width = 46
        hud_height = 11

        examined_object_width = 46
        examined_object_height = term.height - log_height - hud_height - 1

        viewport_width = min((term.width - hud_width, 80))
        viewport_height = min(((term.height - log_height) - 1, 80))

        viewport_pos = (0, 0)
        hud_pos = (viewport_width, 0)
        examined_object_pos = (viewport_width, hud_height)
        log_pos = (0, viewport_height)

        self.board_pane = board.BoardPane(
            viewport_width,
            viewport_height,
            self.mode.world,
            center=self.mode.cursor_pos,
            cursor_attr=(None, colors.bright_green, colors.bright_white)
        )
        self.hud_pane = hud.HUDPane(hud_width, hud_height, self.mode.world)
        self.examined_object_pane = examined_object.ObjectDetailsPane(
            examined_object_width, examined_object_height, self.mode.world
        )
        self.log_pane = log.LogPane(log_width, log_height, self.mode.log)

        self.panes = {
            viewport_pos: self.board_pane,
            hud_pos: self.hud_pane,
            examined_object_pos: self.examined_object_pane,
            log_pos: self.log_pane
        }

    def render(self):
        self.board_pane.center = self.mode.cursor_pos
        self.board_pane.cursor_pos = self.mode.cursor_pos
        self.examined_object_pane.pos = self.mode.cursor_pos
        return super().render()
