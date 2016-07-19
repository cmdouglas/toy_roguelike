from rl.ui.menu import MenuItem
from rl.ui.terminal.modes.menu import SingleSelectMenuMode


class InventoryMode(SingleSelectMenuMode):
    def to_menu_items(self, items):
        return [MenuItem(k, v) for k, v in items.to_keyed_list()]