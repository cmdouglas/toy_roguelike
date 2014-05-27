import logging
from lib.engines.libtcod import libtcodpy as libtcod

class InputKey(object):
    def __init__(self,k):
        self.c = k.c
        self.vk = k.vk
        self.ctrl = k.lctrl or k.rctrl
        self.alt = k.lalt or k.ralt

def wait_for_keypress(win=None):
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    
    libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS, key, mouse, True)
    logging.debug("Key: c: %s, vk: %s, lalt: %s, ralt: %s, lctrl: %s, rctrl: %s" % (key.c, key.vk, key.lalt, key.ralt, key.lctrl, key.rctrl))
    
    return InputKey(key)