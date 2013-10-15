import config

if config.engine == "libtcod":
    from lib.engines.libtcod.libtcodpy import (
        black,
        white,
        dark_gray,
        light_gray,
        red,
        dark_red,
        green,
        light_green,
        blue,
        dark_blue,
        sepia,
        yellow,
        cyan,
        light_cyan,
        purple,
        magenta
    )
    
elif config.engine == "curses":
    from lib.engines.curses.colors import (
        black,
        white,
        dark_gray,
        light_gray,
        red,
        dark_red,
        green,
        light_green,
        blue,
        dark_blue,
        sepia,
        yellow,
        cyan,
        light_cyan,
        purple,
        magenta
    )
    