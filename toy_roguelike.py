import sys
sys.path.append("lib")

import libtcodpy as libtcod
import numpy
import logging

from gameobjects.player import Player
from gameobjects.wall import Wall
from board.testboard import BasicBoard, TestCavern, TestCircle
from errors import GameEndException

SCREEN_WIDTH=80
SCREEN_HEIGHT=50
LIMIT_FPS=10
MAIN_CONSOLE = 0

con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
blank = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
for y in range(SCREEN_HEIGHT):
    for x in range(SCREEN_WIDTH):
        libtcod.console_set_default_foreground(blank, libtcod.white)
        libtcod.console_put_char(blank, x, y, ' ', libtcod.BKGND_NONE)

libtcod.console_set_custom_font('fonts/terminal10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)

def handle_keys():
    key = libtcod.console_check_for_keypress()
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return True

def draw_board(board, center):
    c_x, c_y = center
    ul_x = 0
    ul_y = 0
    
    if c_x > board.width - SCREEN_WIDTH / 2:
        logging.debug('sticking to right side')
        ul_x = board.width - SCREEN_WIDTH
    elif c_x <= SCREEN_WIDTH / 2:
        logging.debug('sticking to left side');
        ul_x = 0
    else:
        ul_x = c_x - SCREEN_WIDTH / 2
        
    if c_y > board.height - SCREEN_HEIGHT / 2:
        logging.debug('sticking to bottom')
        ul_y = board.height - SCREEN_HEIGHT
    elif c_y <= SCREEN_HEIGHT / 2:
        logging.debug('sticking to top')
        ul_y = 0;
    else:
        ul_y = c_y - SCREEN_HEIGHT / 2
        
    #clear screen by blitting a blank console onto it.
    libtcod.console_blit(blank, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, MAIN_CONSOLE, 0, 0)
    
    #draw screen
    for x, row in enumerate(board.tiles[ul_x:(ul_x + SCREEN_WIDTH)]):
        for y, tile in enumerate(row[ul_y:(ul_y + SCREEN_HEIGHT)]):
 
            char, color, bgcolor = tile.draw()
            
            # logging.info('drawing "%s" at %s' % (char, (x, y)));
            
            libtcod.console_set_default_foreground(con, color)
            libtcod.console_put_char(con, x, y, char, libtcod.BKGND_NONE)
    
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, MAIN_CONSOLE, 0, 0)
    libtcod.console_flush()
        
 
def game_loop():
    logging.info("generating board")
    board = TestCircle(90, 60)
    logging.info("board generated")
    center = board.player_pos
    draw_board(board, center)
    while not libtcod.console_is_window_closed():
        try:
            for ob in board.objects:
                if ob.can_act:
                    changed = ob.process_turn()
                    if changed:
                        center = board.player_pos
                        draw_board(board, center)
        except(GameEndException):
            break


            
def main():
    logging.basicConfig(filename='log/rltest.log', level=logging.DEBUG)
    
    logging.info('Game Start')
    game_loop()
    logging.info('Game End')
    
            
if __name__ == '__main__':
    main()
