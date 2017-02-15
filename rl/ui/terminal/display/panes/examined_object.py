import logging

from rl.ui.terminal.display import colors
from rl.ui.terminal.display.render.tile import visible_entity, render_tile
from termapp.formatstring import FormatString
from termapp.layout import Pane

logger = logging.getLogger('rl')


class ObjectDetailsPane(Pane):
    def __init__(self, width, height, world, pos=(0, 0)):
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

        if self.pos in self.world.board.visible:
            seen = True
            see = "  You can see here:"
            tile = self.world.board[self.pos]
            ent = visible_entity(tile)

            if ent:
                glyph, color, bgcolor = render_tile(tile)
                desc = ent.describe()

        elif self.pos in self.world.board.remembered:
            seen = True
            see = "  You remember seeing here:"
            tile = self.world.board[self.pos]
            remembered_tile = self.world.board.remembered[self.pos]
            glyph, color, bgcolor = render_tile(tile)
            ent = visible_entity(remembered_tile)
            desc = ent.describe()

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
