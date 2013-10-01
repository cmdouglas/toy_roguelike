import curses

SIMPLE_KEYS = set([ord(c) for c in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"])

class InputKey(object):
    def __init__(self, c, vk=0, alt=False, ctrl=False):
        self.c = c
        self.vk = vk
        self.alt = alt
        self.ctrl = ctrl
        

def wait_for_keypress(win=None):
    key = win.getch()
    if key in SIMPLE_KEYS:
        return InputKey(key)
    