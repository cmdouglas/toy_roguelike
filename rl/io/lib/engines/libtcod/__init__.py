import rl.lib.engines.libtcod.libtcodpy
def is_running():
    return not rl.lib.engines.libtcod.libtcodpy.console_is_window_closed()