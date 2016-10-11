import logging

from termapp.layout import Layout
from termapp.term import term

from rl.ui.terminal.display.panes import board
from rl.ui.terminal.display.panes import log as log_mod
from rl.ui.terminal.display.panes import hud
from rl.ui.terminal.display.panes import objects_of_interest

logger = logging.getLogger('rl')


class WorldModeLayout(Layout):
    def __init__(self, world):
        super().__init__()
        self.world = world

        log_width = term.width
        log_height = 4

        hud_width = 46
        hud_height = 11

        ooi_width = 46
        ooi_height = term.height - log_height - hud_height - 1

        viewport_width = min((term.width - hud_width, 80))
        viewport_height = min(((term.height - log_height) - 1, 80))

        viewport_pos = (0, 0)
        hud_pos = (viewport_width, 0)
        ooi_pos = (viewport_width, hud_height)
        log_pos = (0, viewport_height)

        self.board_pane = board.BoardPane(viewport_width, viewport_height, self.world)
        self.hud_pane = hud.HUDPane(hud_width, hud_height, self.world)
        self.ooi_pane = objects_of_interest.ObjectsOfInterestPane(
            ooi_width, ooi_height, self.world
        )
        self.log_pane = log_mod.LogPane(log_width, log_height, self.world.messages)

        self.panes = {
            viewport_pos: self.board_pane,
            hud_pos: self.hud_pane,
            ooi_pos: self.ooi_pane,
            log_pos: self.log_pane
        }

    def render(self):
        self.board_pane.center = self.world.player.tile.pos
        return super().render()
