import logging

from rl.ui import tools as ui_tools
from rl.ui.terminal.display import colors
from rl.ui.terminal.display.render.entities.renderer import EntityRenderer
from rl.util.mixins.stackable import Stackable
from termapp.formatstring import FormatString
from termapp.layout import Pane


logger = logging.getLogger('rl')


class ObjectsOfInterestPane(Pane):
    def __init__(self, width, height, world):
        super().__init__(width, height)
        self.world = world
        self.entity_renderer = EntityRenderer()

    def draw_objects_of_interest(self):
        oois = ui_tools.entities_by_type(ui_tools.interesting_entities(self.world))
        oois.sort(key=lambda l: l[0].interest_level, reverse=True)
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

        for i, ents in enumerate(oois[:(self.height-1)]):
            if isinstance(ents[0], Stackable):
                count = sum([ent.stack_size for ent in ents])
            else:
                count = len(ents)

            description = ents[0].describe(num=count)
            glyphs = []
            for ent in ents[:5]:
                glyph, color, bgcolor = self.entity_renderer.render(ent, ent.tile)
                glyphs.append(FormatString().simple(
                    glyph, color=color, bgcolor=bgcolor
                ))

            line = (FormatString("  ") +
                    FormatString().join("", glyphs) +
                    FormatString(": {desc}".format(desc=description)))

            self.set_line(i+1, line)

    def refresh(self):
        self.draw_objects_of_interest()
