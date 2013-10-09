import curses
from lib.engines.curses.colors import CursesColorPair
import locale
locale.setlocale(locale.LC_ALL,"")

import logging
class Renderer(object):
    def __enter__(self):
        self.scr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.scr.keypad(1)
        
        self.height, self.width = self.scr.getmaxyx()
        
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        curses.nocbreak(); 
        self.scr.keypad(0); 
        curses.echo()
        curses.endwin()
        
    def clear(self):
        pass
        
    def draw(self, board, center):
        c_x, c_y = center
        ul_x = 0
        ul_y = 0
    
        if c_x > board.width - self.width / 2:
            ul_x = board.width - self.width
        elif c_x <= self.width / 2:
            ul_x = 0
        else:
            ul_x = c_x - self.width / 2
        
        if c_y > board.height - self.height / 2:
            ul_y = board.height - self.height
        elif c_y <= self.height / 2:
            ul_y = 0;
        else:
            ul_y = c_y - self.height / 2
            
        self.clear()
            
        #draw screen
        for x, row in enumerate(board.tiles[ul_x:(ul_x + self.width)]):
            for y, tile in enumerate(row[ul_y:(ul_y + self.height)]):
            
                char, color, bgcolor = tile.draw()
                
                colorpair = CursesColorPair(color, bgcolor)
                try:
                    self.scr.addstr(y, x, char, colorpair.attr())
                except curses.error:
                    pass
        
        self.scr.refresh()

        
    