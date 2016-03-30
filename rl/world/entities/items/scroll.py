import random

from rl.world.entities.items import Item
from rl.world.events.movement import TeleportEvent

class Scroll(Item):
    type = 'scroll'
    usable = True
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
    type = 'teleportation_scroll'
    name = "teleportation scroll"
    name_plural = "teleportation scrolls"
    interest_level = 5

    def use_effect(self, actor):
        board = actor.tile.board
        region = random.choice(board.regions)
        new_pos = random.choice(region.empty_points())
        old_pos = actor.tile.pos
        new_x, new_y = new_pos
        old_x, old_y = old_pos

        actor.move((new_x-old_x, new_y-old_y))

        actor.inventory.remove(item=self)
        return [TeleportEvent(actor, old_pos, new_pos)]
