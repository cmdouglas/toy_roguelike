import random

from rl.entities.items import Item
from rl.ui import colors
from rl.events.movement import TeleportEvent

class Scroll(Item):
    usable = True
    glyph = '?'
    color = colors.bright_white

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
        area = random.choice(board.areas)
        new_pos = random.choice(area.get_empty_points())
        old_pos = actor.tile.pos

        board.move_entity(actor, old_pos, new_pos)

        actor.inventory.remove(item=self)
        return [TeleportEvent(actor, old_pos, new_pos)]
