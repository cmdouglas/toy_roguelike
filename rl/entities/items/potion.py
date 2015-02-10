from rl.ui import colors
from rl.util import dice
from rl.entities import items


class Potion(items.Item):
    usable = True
    glyph = '!'
    name = "potion"

    def use_effect(self, actor, world):
        pass

    def throw_effect(self, actor, world):
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

    def __init__(self, num=1):
        self.stack_size = num

    def use_effect(self, actor, world):
        actor.heal(dice.d(2, 8))
        actor.inventory.remove(item=self)
