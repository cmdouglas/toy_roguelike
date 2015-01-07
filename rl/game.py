import logging

from rl import globals as G
from rl.ui.lib.engines.curses import render
from rl.modes import gamemode

class Game(object):
    def __init__(self, config):
        pass

    def play(self):
        with render.Renderer() as r:
            G.renderer = r
            mode = gamemode.GameMode()
            mode.process()
        
    def end(self):
        pass