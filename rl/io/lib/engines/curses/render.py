import curses
import os

from rl.io import colors
from rl.io.hud import HUD
from rl.io.lib.engines.curses.colors import CursesColorPair

import logging

class Renderer(object):
    def __enter__(self):
        os.putenv('ESCDELAY', '10')
        self.scr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.scr.keypad(1)
        self.height, self.width = self.scr.getmaxyx()
        
        assert self.height >= 24
        assert self.width >= 80
        

        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        curses.nocbreak(); 
        self.scr.keypad(0); 
        curses.echo()
        curses.endwin()
