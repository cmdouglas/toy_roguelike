from rl.ui.terminal.modes import Mode
from rl.ui.terminal.modes.menu import layout
from rl.ui import menu
from rl.ui.terminal.modes.menu import commands

from termapp.term import term


class SingleSelectMenuMode(Mode):
    def __init__(self, items, selected_callback=None,
                 empty="", exit_on_select=True):
        super().__init__()
        self.menu = menu.Menu(items, empty=empty)
        self.exit_on_select = exit_on_select
        self.selected_callback = selected_callback
        self.layout = layout.MenuModeLayout(self.menu)
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
        if self.exit_on_select:
            self.exit()

        if item and self.selected_callback:
            self.selected_callback(item)


class MultiSelectMenuMode():
    pass
