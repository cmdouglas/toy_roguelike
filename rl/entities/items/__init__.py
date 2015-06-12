from rl.entities import Entity
from rl.util.mixins.stackable import Stackable


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
        if self.stack_size == 1:
            return "{article} {name}".format(article=self.article, name=self.name)
        else:
            return "{num} {name_plural}".format(num=self.stack_size, name_plural=self.name_plural)

    def describe_use(self, third_person=False):
        return ""

    def __str__(self):
        return self.describe()
