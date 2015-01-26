import random

from rl import globals as G
from rl.entities.items import Item
from rl.ui import colors


class Scroll(Item):
    usable = True
    glyph = '?'
    color = colors.bright_white

    def use_effect(self, actor):
        pass


class TeleportationScroll(Scroll):
    name = "teleportation scroll"
    name_plural = "teleportation scrolls"
    interest_level = 5

    def use_effect(self, actor):
        area = random.choice(G.world.board.areas)
        new_pos = random.choice(area.get_empty_points())
        old_pos = actor.tile.pos

        G.world.board.move_entity(actor, old_pos, new_pos)
        G.ui.console.add_message("Your surroundings suddenly seem different",
                                 color=colors.bright_cyan)

        actor.inventory.remove(item=self)
