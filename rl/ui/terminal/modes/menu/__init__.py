from rl import globals as G
from rl.ui.terminal.modes import Mode
from rl.ui.terminal.modes.menu import commands
from rl.ui.terminal.display.layouts import menumodelayout
from rl.ui import menu

class SingleSelectMenuMode(Mode):
    def __init__(self, items, selected_callback=None, empty="", exit_on_select=True):
        super().__init__()
        self.menu = menu.Menu(items, empty=empty)
        self.exit_on_select = exit_on_select
        self.selected_callback=selected_callback
        self.layout = menumodelayout.MenuModeLayout(self.menu)

    def newframe(self):
        if self.child_mode:
            return self.child_mode.newframe()

        return self.layout.render()

    def handle_keypress(self, key):
        command = commands.get_user_command(key)
        if not command:
            return

        result = command.process(self.menu)

        if isinstance(command, commands.SelectCommand) and result:
            self.handle_select(result)

        if isinstance(command, commands.ExitMenuCommand):
            self.exit()

    def handle_select(self, item):

        if self.exit_on_select:
            self.exit()

        if item and self.selected_callback:
            self.selected_callback(item)


class MultiSelectMenuMode():
    pass

