from termapp import application

from rl.ui.terminal.modes.game import GameMode
from rl.ui.console import Console


class TerminalUI(application.TerminalApplication):
    def __init__(self):
        super().__init__()
        self.mode = GameMode()
        self.console = Console()

    def newframe(self):
        return self.mode.newframe()

    def handle_keypress(self, key):
        return self.mode.handle_keypress(key)
