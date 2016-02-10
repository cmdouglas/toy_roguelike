from rl.ui.terminal.log import Log
from rl.ui.terminal.modes.menu import SingleSelectMenuMode
from rl.ui.terminal.modes.world import WorldMode
from termapp import application


class TerminalUIException(Exception):
    pass


class TerminalUI(application.TerminalApplication):
    """
    The game terminal UI is conceived as a stack of modes.  Keystrokes and
    rendering are handled by the top mode on the stack.  When a mode exits, it
    is popped off of the stack, and any closing work is handled in its
    on_exit() method.  When the stack is empty, the game exits.
    """

    def __init__(self):
        super().__init__()
        self.modes = []
        self.log = Log()

    def on_start(self):
        self.enter_mode(WorldMode())

    def next_frame(self):
        # this should never happen, since the game would exit when the last
        # mode exits, but handle it anyway.
        if not self.modes:
            raise TerminalUIException("There are no modes to render a frame.")

        return self.modes[0].next_frame()

    def handle_keypress(self, key):
        # this should never happen, since the game would exit when the last
        # mode exits, but handle it anyway.
        if not self.modes:
            raise TerminalUIException(
                "There are no modes to handle a keypress."
            )

        return self.modes[0].handle_keypress(key)

    def enter_mode(self, mode):
        mode.owner = self
        self.modes.insert(0, mode)
        mode.on_enter()

    def exit_mode(self):
        mode = self.modes.pop(0)
        mode.on_exit()
        mode.owner = None

        if not self.modes:
            raise application.StopApplication()

        self.modes[0].on_reenter()
