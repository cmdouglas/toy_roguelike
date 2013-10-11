import curses
from io import colors
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
        
        assert self.height >= 24
        assert self.width >= 80
        
        self.viewport_height = self.height - 5
        self.viewport_width = self.width - 46
        self.console_width = self.width
        self.console_height = 5
        self.stats_width = 46
        self.stats_height = self.height - 5
        
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        curses.nocbreak(); 
        self.scr.keypad(0); 
        curses.echo()
        curses.endwin()
        
    def clear(self):
        pass
        
    def draw(self, board, center, console, stats):
        self.draw_viewport(board, center)
        self.draw_console(console)
        self.draw_stats(stats)
        
        self.scr.refresh()
        
    def draw_stats(self, stats):
        pass
        
    def draw_console(self, console):
        console_pad = curses.newpad(self.console_height, self.console_width)
        lines = console.get_last_lines(num_lines=self.console_height)
        
        for i, line in enumerate(lines):
            colorpair = CursesColorPair(line['color'], colors.black)
            console_pad.addstr(i, 0, line['message'], colorpair.attr())
            
        console_pad.refresh(
            0, 0,                       #pad ul_corner coords 
            self.viewport_height, 0,    #screen ul_corner coords
            self.height-1,self.width-1  #screen lr_corner coords
        )
        
    def draw_viewport(self, board, center):
        c_x, c_y = center
        ul_x = 0
        ul_y = 0
    
        if c_x > board.width - self.viewport_width / 2:
            ul_x = board.width - self.viewport_width
        elif c_x <= self.viewport_width / 2:
            ul_x = 0
        else:
            ul_x = c_x - self.viewport_width / 2
        
        if c_y >= board.height - self.viewport_height / 2:
            ul_y = board.height - self.viewport_height
        elif c_y < self.viewport_height / 2:
            ul_y = 0;
        else:
            ul_y = c_y - self.viewport_height / 2
                        
        for x, row in enumerate(board.tiles[ul_x:(ul_x + self.viewport_width)]):
            for y, tile in enumerate(row[ul_y:(ul_y + self.viewport_height)]):
            
                char, color, bgcolor = tile.draw()
                
                colorpair = CursesColorPair(color, bgcolor)
                try:
                    self.scr.addstr(y, x, char, colorpair.attr())
                except curses.error:
                    pass
        
        
    