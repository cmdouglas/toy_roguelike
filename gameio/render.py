import config

if config.engine == "libtcod":
    from lib.engines.libtcod import render
    
elif config.engine == 'curses':
    from lib.engines.curses import render