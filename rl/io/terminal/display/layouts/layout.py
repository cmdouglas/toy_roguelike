from rl import globals as G
from rl.io.terminal.display.panes import pane

class Layout(object):
    def __init__(self):
        self.panes = {}
        self.container = pane.Pane(G.renderer.width, G.renderer.height)

    def render(self):
        if not self.container.subpanes:
            self.container.subpanes = self.panes

        return self.container.render()