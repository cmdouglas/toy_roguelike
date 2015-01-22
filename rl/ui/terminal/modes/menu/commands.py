import logging

from rl import globals as G
from rl.ui import commands

logger = logging.getLogger('rl')


def get_user_command(keypress):

    term = G.ui.term
    commands = {
        term.KEY_UP: MoveSelectedCommand(1),
        term.KEY_DOWN: MoveSelectedCommand(-1),
        term.KEY_ESCAPE: ExitMenuCommand(),
        term.KEY_ENTER: SelectCommand()
    }

    if keypress.is_sequence:
        code = keypress.code

    else:
        code = ord(str(keypress))

    return commands.get(code, SelectCommand(code))


class MenuModeCommand(commands.Command):
    pass


class MoveSelectedCommand(MenuModeCommand):
    def __init__(self, d, n=1):
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
        pass


class SelectCommand(MenuModeCommand):
    def __init__(self, key=None):
        self.key = key

    def process(self, menu):
        selected = menu.get_selected(key=self.key)
        return selected
