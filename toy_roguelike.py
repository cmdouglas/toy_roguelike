import libtcodpy as libtcod
import logging

from gameobjects.player import Player
from gameobjects.wall import Wall
from board.testboard import BasicBoard, TestCavern, TestCircle
from errors import GameEndException

SCREEN_WIDTH=80
SCREEN_HEIGHT=50
LIMIT_FPS=20
MAIN_CONSOLE = 0

con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

libtcod.console_set_custom_font('fonts/terminal10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)

def handle_keys():
    key = libtcod.console_check_for_keypress()
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return True

def draw_board(board):
    for row in board.tiles:
        for tile in row:
            x, y = tile.pos
            char, color, bgcolor = tile.draw()
            
            libtcod.console_set_default_foreground(con, color)
            libtcod.console_put_char(con, x, y, char, libtcod.BKGND_NONE)
    
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, MAIN_CONSOLE, 0, 0)
    libtcod.console_flush()
        
 
def game_loop():
    logging.info("generating board")
    board = TestCircle(80, 45)
    draw_board(board)
    while not libtcod.console_is_window_closed():
        try:
            for ob in board.objects:
                if ob.can_act:
                    changed = ob.process_turn()
                    if changed:
                        draw_board(board)
        except(GameEndException):
            break


            
def main():
    logging.basicConfig(filename='log/rltest.log', level=logging.DEBUG)
    
    logging.info('Game Start')
    game_loop()
    logging.info('Game End')
    
            
if __name__ == '__main__':
    main()
