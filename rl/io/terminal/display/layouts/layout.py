import curses
from rl import globals as G

class Layout(object):
    def __init__(self):
        self.panes = {}
        self.main_pane = None

    def render(self):
        for pos, pane in self.panes.items():
            pane.render(pos)

        curses.doupdate()

