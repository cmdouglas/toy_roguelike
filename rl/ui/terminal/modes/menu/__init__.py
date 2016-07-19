import logging

from rl.ui.terminal.modes import Mode
from rl.ui.terminal.modes.menu.layout import MenuModeLayout
from rl.ui.menu import Menu
from rl.ui.terminal.modes.menu import commands

from termapp.term import term

logger = logging.getLogger('rl')


class BaseMenuMode(Mode):
    def __init__(self):
        super().__init__()

        self.menu = Menu([], empty_msg="")
        self.exit_on_select = False
        self.on_select = None
        self.layout = MenuModeLayout(self.menu)
        self.changed = True

        self.commands = {
            term.KEY_UP: commands.MoveSelectedCommand(self, 1),
            term.KEY_DOWN: commands.MoveSelectedCommand(self, -1),
            term.KEY_ESCAPE: commands.ExitMenuCommand(self),
            term.KEY_ENTER: commands.SelectCommand(self)
        }

    def next_frame(self):
        if self.changed:
            self.changed = False
            return self.layout.render()

    def handle_keypress(self, key):
        logger.debug('BaseMenuMode: Recieved keypress ' + str(key))
        if key.is_sequence:
            letter = None
            code = key.code

        else:
            letter = str(key)
            code = ord(letter)

        command = self.commands.get(code, commands.SelectCommand(self, key=letter))

        if not command:
            return

        command.process(self.menu)

    def handle_select(self, item):
        if item and self.on_select:
            self.on_select(item.item)

        if self.exit_on_select:
            self.exit()

    def on_enter(self):
        if self.owner:
            self.owner.screen.clear()
            self.owner.term.clear()

    def on_reenter(self):
        if self.owner:
            self.owner.screen.clear()
            self.owner.term.clear()


class SingleSelectMenuMode(BaseMenuMode):
    def __init__(self, items, empty_msg="", on_select=None, exit_on_select=False):
        super().__init__()
        self.menu.items = self.to_menu_items(items)
        self.menu.empty_msg = empty_msg
        self.on_select = on_select
        self.exit_on_select = exit_on_select

    def to_menu_items(self, items):
        return items


class MultiSelectMenuMode():
    pass
