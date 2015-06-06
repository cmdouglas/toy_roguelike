from collections import OrderedDict

from rl.util.mixins.stackable import Stackable


class KeyedStackableBag:
    keys = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def __init__(self):
        self.items = OrderedDict()
        for k in self.keys:
            self.items[k] = None

    def add(self, item, force_key=None):
        assert isinstance(item, Stackable)

        if force_key and not self.items.get(force_key):
            self.items[force_key] = item

        # If there's already a stack of this type in the bag, add to it.
        for key, item_ in self.items.items():
            if type(item_) == type(item):
                self.items[key].merge_with_stack(item)
                return

        # Create a new stack of this type on the first empty key.
        new_key = None
        for k in self.keys:
            if self.items[k]:
                continue

            new_key = k
            break

        if not new_key:
            raise BagFullException("full")

        self.items[new_key] = item

    def remove(self, key=None, item=None, count=1):
        if key is None:
            for k, item_ in self.items.items():
                if type(item) == type(item_):
                    key = k

        if key and self.items[key]:
            r = self.items[key].pop_from_stack(count)

            if self.items[key].is_empty():
                self.items[key] = None

            return r

    def to_dict(self):
        d = {}
        for k, v in self.items.items():
            if v:
                d[k] = v

        return d

    @classmethod
    def from_list(cls, l):
        bag = cls()
        for item in l[:len(bag.keys)]:
            bag.add(item)


class BagFullException(Exception):
    pass
