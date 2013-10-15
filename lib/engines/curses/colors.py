import curses
import logging

class CursesColor(object):
    def __init__(self, color, bright=False):
        self.color = color
        self.bright = bright

    def __str__(self):
        return "COLOR(%s, %s)" % (self.color, self.bright)
color_pairs = {}
color_pair_num = 1

class CursesColorPair(object):
    def __init__(self, fg, bg):
        global color_pair_num, color_pairs
        self.fg = fg
        self.bg = bg
        self.color_pair_num = color_pairs.get((fg, bg))
        
        if not self.color_pair_num:
            curses.init_pair(color_pair_num, fg.color, bg.color)
            color_pairs[(fg, bg)] = color_pair_num
            self.color_pair_num = color_pair_num
            
            color_pair_num += 1
            
    def attr(self):
        #logging.debug("self.color_pair_num: %s" % self.color_pair_num)
        a = curses.color_pair(self.color_pair_num)
        if self.fg.bright:
            a = a | curses.A_BOLD
            
        return a
        
    def __str__(self):
        return "COLORPAIR(%s, %s)" % (self.fg, self.bg)
    
black = CursesColor(curses.COLOR_BLACK)
dark_gray = CursesColor(curses.COLOR_BLACK, bright=True)
light_gray = CursesColor(curses.COLOR_WHITE)
white = CursesColor(curses.COLOR_WHITE, bright=True)
dark_red = CursesColor(curses.COLOR_RED)
red = CursesColor(curses.COLOR_RED, bright=True)
green = CursesColor(curses.COLOR_GREEN)
light_green = CursesColor(curses.COLOR_GREEN, bright=True)
sepia = CursesColor(curses.COLOR_YELLOW)
yellow = CursesColor(curses.COLOR_YELLOW, bright=True)
dark_blue = CursesColor(curses.COLOR_BLUE)
blue = CursesColor(curses.COLOR_BLUE, bright=True)
purple = CursesColor(curses.COLOR_MAGENTA)
magenta = CursesColor(curses.COLOR_MAGENTA, bright=True)
cyan = CursesColor(curses.COLOR_CYAN)
light_cyan = CursesColor(curses.COLOR_CYAN, bright=True)