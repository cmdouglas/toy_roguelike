import curses
import logging

from rl import globals as G

SIMPLE_KEYS = set([ord(c) for c in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"])

KEY_UP = curses.KEY_UP
KEY_DOWN = curses.KEY_DOWN
KEY_LEFT = curses.KEY_LEFT
KEY_RIGHT = curses.KEY_RIGHT

KEY_ENTER = 10

KEY_ESC = 361

class InputKey(object):
    def __init__(self, c, vk=0, alt=False, ctrl=False):
        self.c = c
        self.vk = vk
        self.alt = alt
        self.ctrl = ctrl
        

def wait_for_keypress():
    win = G.renderer.scr
    key = win.getch()
    #logging.debug(key)
    if key in SIMPLE_KEYS or key in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_ENTER]:
        return InputKey(key)

    elif key == 27:
        win.nodelay(True)
        n = win.getch()

        win.nodelay(False)
        if n == -1:
            return InputKey(KEY_ESC)

        else:
            return InputKey(n, alt=True)

        
    
    
    