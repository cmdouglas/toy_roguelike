from termapp.layout import Layout
from termapp.term import term

from rl.ui.terminal.display.panes.prompt import PromptPane

class PromptModeLayout(Layout):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.refresh()

    def refresh(self):
        self.panes = {
            (0,0): PromptPane(term.width, term.height, self.mode)
        }