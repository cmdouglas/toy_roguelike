import libtcodpy as libtcod

from errors import GameEndException
from gameobjects.base import Actor

class Player(Actor):
    color = libtcod.white
    char = '@'
    
    def process_turn(self):
        key = libtcod.console_wait_for_keypress(True)
        #movement keys
        if key.vk == libtcod.KEY_UP or key.c == ord('k'):
            self.move(0, -1)
    
        elif key.vk == libtcod.KEY_DOWN or key.c == ord('j'):
            self.move(0, 1)
    
        elif key.vk == libtcod.KEY_LEFT or key.c == ord('h'):
            self.move(-1, 0)
    
        elif key.vk == libtcod.KEY_RIGHT or key.c == ord('l'):
            self.move(1, 0)
            
        elif key.c == ord('y'):
            self.move(-1, -1)

        elif key.c == ord('u'):
            self.move(1, -1)
            
        elif key.c == ord('b'):
            self.move(-1, 1)

        elif key.c == ord('n'):
            self.move(1, 1)
            
        if key.vk == libtcod.KEY_ENTER and key.lalt:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        elif key.vk == libtcod.KEY_ESCAPE:
            raise GameEndException()
                
        return True
    