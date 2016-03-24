from rl.util import dice
from rl.world.entities.items import Item

from rl.world.events.health import GainHealthEvent


class Potion(Item):
    type = 'potion'
    usable = True
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
    type = 'healing_potion'
    name = "healing potion"
    name_plural = "healing potions"
    interest_level = 8

    def use_effect(self, actor):
        amount = dice.d(2, 8)
        actor.heal(amount)
        actor.inventory.remove(item=self)
        return [GainHealthEvent(actor, amount)]
