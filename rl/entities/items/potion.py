from rl.save import rl_types
from rl.ui import colors
from rl.util import dice
from rl.entities.items import Item, dump_item, load_item

from rl.events.health import GainHealthEvent


class Potion(Item):
    usable = True
    glyph = '!'
    name = "potion"
    name_plural = "potions"

    def use_effect(self, actor):
        pass

    def throw_effect(self, actor):
        pass

    def describe_use(self, third_person=False):
        if third_person:
            return "drinks"
        else:
            return "drink"


class HealingPotion(Potion):
    color = colors.bright_yellow
    name = "healing potion"
    name_plural = "healing potions"
    interest_level = 8

    def use_effect(self, actor):
        amount = dice.d(2, 8)
        actor.heal(amount)
        actor.inventory.remove(item=self)
        return [GainHealthEvent(actor, amount)]


@rl_types.dumper(HealingPotion, 'healing_potion', 1)
def _dump_healing_potion(healing_potion):
    return dump_item(healing_potion)


@rl_types.loader('healing_potion', 1)
def _load_healing_potion(data, version):
    healing_potion = HealingPotion()
    load_item(data, healing_potion)

    return healing_potion