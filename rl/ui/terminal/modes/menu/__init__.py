

class SingleSelectMenuMode():
    def __init__(self, items):
        self.items = items

    def select_item(self, item):
        pass

    def exit(self):
        pass


class MultiSelectMenuMode():
    pass


class ViewItemsMode(SingleSelectMenuMode):
    """Used for looking at inventory"""

    def exit(self):
        pass