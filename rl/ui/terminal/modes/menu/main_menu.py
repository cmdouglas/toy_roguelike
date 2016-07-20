import logging

from rl.ui.menu import MenuItem
from rl.ui.terminal.modes.game import GameMode
from rl.ui.terminal.modes.menu.load_menu import LoadGameMenuMode
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
        self.owner.enter_mode(GameMode())

    def select_game_to_continue(self):
        self.owner.enter_mode(LoadGameMenuMode())

    def exit_game(self):
        self.exit()
