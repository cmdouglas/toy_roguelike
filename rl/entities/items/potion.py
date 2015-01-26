from rl import globals as G
from rl.ui import colors
from rl.util import dice
from rl.entities import items


class Potion(items.Item):
    usable = True
    glyph = '!'

    def use_effect(self, actor):
        pass

    def throw_effect(self, actor):
        pass


class HealingPotion(Potion):
    color = colors.bright_yellow
    name = "healing potion"
    name_plural = "healing potions"
    interest_level = 8

    def __init__(self, num=1):
        self.stack_size = num

    def use_effect(self, actor):
        actor.heal(dice.d(2, 8))
        G.ui.console.add_message('You feel better.', colors.bright_yellow)

        actor.inventory.remove(item=self)
