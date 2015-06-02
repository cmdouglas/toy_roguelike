
import logging

from termapp.layout import Pane
from termapp.formatstring import FormatString

from rl.ui.hud import HUD
from rl.ui import colors

logger = logging.getLogger('rl')


class ObjectDetailsPane(Pane):
    def __init__(self, width, height, world, object=None, pos=(0,0)):
        super().__init__(width, height)
        self.world = world

    def draw_object_details(self):

        self.set_line(
            0, FormatString().simple("  You can see:", color=colors.cyan)
        )

    def refresh(self):
        self.draw_object_details()
