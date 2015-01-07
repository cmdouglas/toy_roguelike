import logging

from rl import globals as G
from rl.modes import mode
from rl.ui import commands
from rl.ui.lib.engines.curses import keypress

def get_user_command():
    k = keypress.wait_for_keypress()

    commands = {
        keypress.KEY_UP: MoveSelectedCommand(1),
        keypress.KEY_DOWN: MoveSelectedCommand(-1),
        keypress.KEY_ESC: ExitMenuCommand(),
        keypress.KEY_ENTER: SelectCommand()

    }
    if k:
        return commands.get(k.c)

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
        raise mode.ModeExitException()

class SelectCommand(MenuModeCommand):
    def process(self, m):
        selected = m.get_selected()
        return selected