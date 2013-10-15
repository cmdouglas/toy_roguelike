import config

hline = u'\u2500'.encode('utf-8')
vline = u'\u2502'.encode('utf-8')
ne = u'\u2510'.encode('utf-8')
nw = u'\u250c'.encode('utf-8')
se = u'\u2518'.encode('utf-8')
sw = u'\u2514'.encode('utf-8')
tee_n = u'\u2534'.encode('utf-8')
tee_s = u'\u253c'.encode('utf-8')
tee_e = u'\u251c'.encode('utf-8')
tee_w = u'\u2524'.encode('utf-8')
cross = u'\u253c'.encode('utf-8')

dhline = u'\u2550'.encode('utf-8')
dvline = u'\u2551'.encode('utf-8')
dne = u'\u2557'.encode('utf-8')
dnw = u'\u2554'.encode('utf-8')
dse = u'\u255d'.encode('utf-8')
dsw = u'\u255a'.encode('utf-8')
dtee_n = u'\u2569'.encode('utf-8')
dtee_s = u'\u2566'.encode('utf-8')
dtee_e = u'\u2560'.encode('utf-8')
dtee_w = u'\u2563'.encode('utf-8')
dcross = u'\u256c'.encode('utf-8')

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