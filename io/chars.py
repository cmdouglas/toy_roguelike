import config

vline = '|'
hline = '-'
ne = '+'
nw = '+'
se = '+'
sw = '+'
tee_n = '+'
tee_s = '+'
tee_e = '+'
tee_w = '+'
cross = '+'

if config.engine == "libtcod":
    from lib.engines.libtcod import libtcodpy as libtcod
    
    vline = libtcod.CHAR_VLINE
    hline = libtcod.CHAR_HLINE
    ne = libtcod.CHAR_NE
    nw = libtcod.CHAR_NW
    se = libtcod.CHAR_SE
    sw = libtcod.CHAR_SW
    tee_n = libtcod.CHAR_TEEN
    tee_s = libtcod.CHAR_TEES
    tee_e = libtcod.CHAR_TEEE
    tee_w = libtcod.CHAR_TEEW
    cross = libtcod.CHAR_CROSS