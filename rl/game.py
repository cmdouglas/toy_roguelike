
import logging
from rl import globals as G
from rl.ui.terminal import TerminalUI
from rl.world import World



class Game(object):
    def __init__(self, config=None):
        self.world = World()
        G.world = self.world
        G.world.setup()

        self.ui = TerminalUI()
        G.ui = self.ui

    def play(self):
        self.ui.run()
        self.end()
        return

    def end(self):
        pass