
import logging

from termapp.layout import Pane
from termapp.formatstring import FormatString

from rl.ui import colors

logger = logging.getLogger('rl')


class ObjectDetailsPane(Pane):
    def __init__(self, width, height, world, pos=(0,0)):
        super().__init__(width, height)
        self.world = world
        self.object = object
        self.pos = pos

    def draw_object_details(self):
        seen = False
        see = "  You haven't seen this place."
        glyph = ''
        color = None
        bgcolor = None
        desc = ''


        if self.world.board[self.pos].visible:
            seen = True
            see = "  You can see here:"
            tile = self.world.board[self.pos]
            ent = tile.get_visible_entity()

            if ent:
                glyph, color, bgcolor = tile.draw()
                desc = ent.describe()

        elif self.world.board[self.pos].has_been_seen:
            seen = True
            see = "  You remember seeing here:"
            tile = self.world.board[self.pos]
            glyph, color, bgcolor = tile.draw()
            desc = tile.remembered_desc


        self.set_line(
            0, FormatString().simple(see, color=colors.cyan)
        )
        if seen:
            if glyph and desc:
                self.set_line(
                    1, FormatString().simple(
                            "   {glyph}".format(glyph=glyph),
                        color=color,
                        bgcolor=bgcolor) +
                       FormatString().simple(": {desc}".format(desc=desc.capitalize()))
                )
            else:
                self.set_line(
                    1, FormatString().simple("   Nothing of interest.", color=colors.cyan)
                )

    def refresh(self):
        self.clear()
        self.draw_object_details()
