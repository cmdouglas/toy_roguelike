from rl.world.entities import Entity
from rl.util.mixins.stackable import Stackable


class Item(Entity, Stackable):
    type = 'item'
    usable = False
    equippable = False
    article = "a"
    name = ""
    name_plural = ""

    def persist_fields(self):
        fields = super().persist_fields()
        fields.extend(['stack_size'])

    def describe(self, num=0):
        if num == 0:
            num=self.stack_size

        if num == 1:
            return "{article} {name}".format(article=self.article, name=self.name)
        else:
            return "{num} {name_plural}".format(num=num, name_plural=self.name_plural)

    def describe_use(self, third_person=False):
        return ""

    def __str__(self):
        return self.describe()

    def __getstate__(self):
        state = super().__getstate__()
        state.update(self.dump_stackable())
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self.load_stackable(state)