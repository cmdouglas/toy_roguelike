from rl.lib.engines.libtcod import libtcodpy as libtcod

SCREEN_WIDTH=80
SCREEN_HEIGHT=50
LIMIT_FPS=10
MAIN_CONSOLE = 0

class Renderer(object):
    def __enter__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        
        self.con = libtcod.console_new(self.width, self.height)
        self.blank = libtcod.console_new(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                libtcod.console_set_default_foreground(self.blank, libtcod.white)
                libtcod.console_put_char(self.blank, x, y, ' ', libtcod.BKGND_NONE)
                
        libtcod.console_set_custom_font('fonts/terminal10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(self.width, self.height, 'Charlie\'s toy roguelike', False)
        libtcod.sys_set_fps(LIMIT_FPS)
        


        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def clear(self):
        """clear screen by blitting a blank console onto it."""
        libtcod.console_blit(self.blank, 0, 0, self.width, self.height, MAIN_CONSOLE, 0, 0)
        
    def draw(self, board, center):
        c_x, c_y = center
        ul_x = 0
        ul_y = 0
    
        if c_x > board.width - self.width / 2:
            ul_x = board.width - self.width
        elif c_x <= self.width / 2:
            ul_x = 0
        else:
            ul_x = c_x - self.width / 2
        
        if c_y > board.height - self.height / 2:
            ul_y = board.height - self.height
        elif c_y <= self.height / 2:
            ul_y = 0;
        else:
            ul_y = c_y - self.height / 2
            
        self.clear()
            
        #draw screen
        for x, row in enumerate(board.tiles[ul_x:(ul_x + self.width)]):
            for y, tile in enumerate(row[ul_y:(ul_y + self.height)]):
            
                char, color, bgcolor = tile.draw()
                        
                libtcod.console_set_default_foreground(self.con, color)
                libtcod.console_put_char(self.con, x, y, char, libtcod.BKGND_NONE)
    
        libtcod.console_blit(self.con, 0, 0, self.width, self.height, MAIN_CONSOLE, 0, 0)
        libtcod.console_flush()