import libtcodpy as libtcod

def wait_for_keypress():
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    
    libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS, key, mouse, True)
    
    return key
    