from rl.entities.entity import Entity
from rl.util.mixins.stackable import Stackable


class Item(Entity, Stackable):
    usable = False
    equippable = False
    name = ""
    name_plural = ""

    def describe(self):
        if self.stack_size == 1:
            return "%s" % self.name
        else:
            return "stack of %s %s" % (self.stack_size, self.name_plural)

    def __str__(self):
        return self.describe()
