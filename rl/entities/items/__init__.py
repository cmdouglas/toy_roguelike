from rl.entities import Entity
from rl.util.mixins.stackable import Stackable, dump_stackable, load_stackable


class Item(Entity, Stackable):
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


def dump_item(item):
    return dump_stackable(item)


def load_item(data, item):
    load_stackable(data, item)