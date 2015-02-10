from rl.ui.terminal.modes import Mode
from rl.ui.terminal.display.layouts import menumodelayout
from rl.ui import menu

from termapp.term import term


class SingleSelectMenuMode(Mode):
    def __init__(self, items, selected_callback=None,
                 empty="", exit_on_select=True):
        super().__init__()
        self.menu = menu.Menu(items, empty=empty)
        self.exit_on_select = exit_on_select
        self.selected_callback = selected_callback
        self.layout = menumodelayout.MenuModeLayout(self.menu)

        self.commands = {
            term.KEY_UP: MoveSelectedCommand(1),
            term.KEY_DOWN: MoveSelectedCommand(-1),
            term.KEY_ESCAPE: ExitMenuCommand(),
            term.KEY_ENTER: SelectCommand()
        }

    def newframe(self):
        return self.layout.render()

    def handle_keypress(self, key):
        if key.is_sequence:
            letter = None
            code = key.code

        else:
            letter = str(key)
            code = ord(letter)

        command = self.commands.get(code, SelectCommand(letter))

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


class MenuModeCommand():
   def __init__(self, mode):
       self.mode = mode


class MoveSelectedCommand(MenuModeCommand):
    def __init__(self, mode, d, n=1):
        super().__init__(mode)
        self.d = d
        self.n = n

    def process(self, menu):
        for i in range(self.n):
            if self.d == 1:
                menu.move_up()
            else:
                menu.move_down()


class ExitMenuCommand(MenuModeCommand):
    def process(self, menu):
        self.mode.exit()


class SelectCommand(MenuModeCommand):
    def __init__(self, mode, key=None):
        super().__init__(mode)
        self.key = key

    def process(self, menu):
        selected = menu.get_selected(key=self.key)
        if selected:
            self.mode.handle_select(selected)
