import textwrap

from rl.ui.terminal.display import colors


def generate_menu_key():
    keys = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for key in keys:
        yield key


class MenuItem:
    def __init__(self, key, item, description=None):
        self.key = key
        self.item = item
        if description:
            self.description = description
        else:
            self.description = str(item)


class Menu(object):
    def __init__(self, items, empty_msg=""):
        self.items = items

        self.empty_msg = empty_msg
        self.selected = 0

    def move_to(self, key):
        for i, item in enumerate(self.items):
            if item.key == key:
                self.selected = i
                return item
        raise KeyError('%s not found' % key)

    def move_up(self):
        if self.selected > 0:
            self.selected -= 1

    def move_down(self):
        if self.selected < len(self.items) - 1:
            self.selected += 1

    def get_lines(self):
        lines = []

        if not self.items:
            return {
                "line": self.empty_msg,
                "color": colors.white,
                "selected": False
            }

        for i, item in enumerate(self.items):
            ls = textwrap.wrap(item.description)
            ls[0] = item.key + ') ' + ls[0]
            for l in ls:
                lines.append({
                    'line': l,
                    'color': colors.white,
                    'selected': (self.selected == i)
                })

        return lines

    def get_selected(self, key=None):
        item = None
        if not self.items:
            return None

        if key:
            try:
                item = self.move_to(key)
            except KeyError:
                return None

        else:
            item = self.items[self.selected]

        return item
