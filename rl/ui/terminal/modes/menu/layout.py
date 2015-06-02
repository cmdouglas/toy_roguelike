from termapp.layout import Layout
from termapp.term import term

from rl.ui.terminal.display.panes import menu

class MenuModeLayout(Layout):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.refresh()

    def refresh(self):
        self.panes = {
            (0,0): menu.MenuPane(term.width, term.height, self.menu)
        }