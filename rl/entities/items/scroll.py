import random

from rl.entities.items import Item, dump_item, load_item
from rl.ui import colors
from rl.events.movement import TeleportEvent
from rl.save import rl_types

class Scroll(Item):
    usable = True
    glyph = '?'
    color = colors.bright_white
    name = "scroll"
    name_plural = "scrolls"

    def use_effect(self, actor):
        pass


    def describe_use(self, third_person=False):
        if third_person:
            return "reads"

        else:
            return "read"


class TeleportationScroll(Scroll):
    name = "teleportation scroll"
    name_plural = "teleportation scrolls"
    interest_level = 5

    def use_effect(self, actor):
        board = actor.tile.board
        region = random.choice(board.regions)
        new_pos = random.choice(region.empty_points())
        old_pos = actor.tile.pos

        board.move_entity(actor, old_pos, new_pos)

        actor.inventory.remove(item=self)
        return [TeleportEvent(actor, old_pos, new_pos)]


@rl_types.dumper(TeleportationScroll, 'teleportation_scroll', 1)
def _dump_teleportation_scroll(teleportation_scroll):
    return dump_item(teleportation_scroll)


@rl_types.loader('teleportation_scroll', 1)
def _load_teleportation_scroll(data, version):
    teleportation_scroll = TeleportationScroll()
    load_item(data, teleportation_scroll)

    return teleportation_scroll