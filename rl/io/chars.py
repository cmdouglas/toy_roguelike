from rl import config

# blocks
light_block = u'\u2591'
medium_block = u'\u2592'
dark_block = u'\u2593'
full_block = u'\u2588'

#lines 
hline = u'\u2500'
vline = u'\u2502'
ne = u'\u2510'
nw = u'\u250c'
se = u'\u2518'
sw = u'\u2514'
tee_n = u'\u2534'
tee_s = u'\u253c'
tee_e = u'\u251c'
tee_w = u'\u2524'
cross = u'\u253c'

dhline = u'\u2550'
dvline = u'\u2551'
dne = u'\u2557'
dnw = u'\u2554'
dse = u'\u255d'
dsw = u'\u255a'
dtee_n = u'\u2569'
dtee_s = u'\u2566'
dtee_e = u'\u2560'
dtee_w = u'\u2563'
dcross = u'\u256c'


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