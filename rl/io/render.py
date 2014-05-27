from rl import config

if config.engine == "libtcod":
    from rl.lib.engines.libtcod import render
    
elif config.engine == 'curses':
    from rl.lib.engines.curses import render