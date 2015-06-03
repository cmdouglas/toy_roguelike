import logging

from termapp.layout import Pane
from termapp.formatstring import FormatString

from rl.ui.hud import HUD
from rl.ui import colors

logger = logging.getLogger('rl')


class ObjectsOfInterestPane(Pane):
    def __init__(self, width, height, world):
        super().__init__(width, height)
        self.world = world

    def draw_objects_of_interest(self):
        hud = HUD()
        oois = hud.objects_of_interest(self.world)
        # logger.debug(oois)

        self.clear()

        self.set_line(
            0, FormatString().simple("  You can see:", color=colors.cyan)
        )

        if not oois:
            self.set_line(
                1, FormatString().simple(
                    '   Nothing of interest',
                    color=colors.cyan
                )
            )

        for i, ooi in enumerate(oois[:(self.height-1)]):
            line = (
                FormatString().simple(
                    "   {glyphs}".format(glyphs=ooi['glyphs']),
                    color=ooi['color']
                ) +
                FormatString().simple(
                    ": {desc}".format(desc=ooi['description'])
                )
            )

            self.set_line(i+1, line)

    def refresh(self):
        self.draw_objects_of_interest()
