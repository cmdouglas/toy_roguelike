import logging

from rl.ui.menu import MenuItem
from rl.ui.terminal.modes.world import WorldMode
from rl.ui.terminal.modes.menu import BaseMenuMode

logger = logging.getLogger('rl')


class MainMenuMode(BaseMenuMode):
    def __init__(self):
        super().__init__()

        self.menu.items = [
            MenuItem('n', self.new_game, 'New Game'),
            MenuItem('c', self.select_game_to_continue, 'Continue Game'),
            MenuItem('e', self.exit_game, 'Exit')
        ]

        def on_select(item):
            f = item
            f()

        self.on_select = on_select

    def new_game(self):
        self.owner.enter_mode(WorldMode())

    def select_game_to_continue(self):
        pass

    def on_enter(self):
        if self.owner:
            self.owner.screen.clear()

    def on_reenter(self):
        if self.owner:
            self.owner.screen.clear()

    def exit_game(self):
        self.exit()
