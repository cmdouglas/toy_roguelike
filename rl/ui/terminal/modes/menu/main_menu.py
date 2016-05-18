from rl.ui.terminal.modes import Mode
from rl.ui.terminal.modes.world import WorldMode
from rl.ui.terminal.modes.menu import layout
from rl.ui import menu
from rl.ui.terminal.modes.menu import commands

from termapp.term import term


class MainMenuMode(Mode):
    def __init__(self):
        super().__init__()
        items = {


        }
        self.menu = menu.Menu(items)
        self.layout = layout.MenuModeLayout(self.menu)
        self.changed = True

        self.commands = {
            term.KEY_UP: commands.MoveSelectedCommand(self, 1),
            term.KEY_DOWN: commands.MoveSelectedCommand(self, -1),
            term.KEY_ESCAPE: commands.ExitMenuCommand(self),
            term.KEY_ENTER: commands.SelectCommand(self)
        }

    def new_game(self):
        self.owner.enter_mode(WorldMode())

    def select_game_to_continue(self):
        pass

    def exit_game(self):
        pass

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
