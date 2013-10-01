import lib.engines.libtcod.libtcodpy
def is_running():
    return not lib.engines.libtcod.libtcodpy.console_is_window_closed()