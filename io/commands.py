import config
import logging
import game

def get_user_command(game):
    keypress = None
    win = None
    if config.engine == "libtcod":
        from lib.engines.libtcod import keypress
    elif config.engine == "curses":
        from lib.engines.curses import keypress
        win = game.renderer.scr
        
    k = keypress.wait_for_keypress(win)
    
    commands = {
        # movement
        ord('h'): MoveOrAttackCommand((-1, 0)),
        ord('j'): MoveOrAttackCommand((0, 1)),
        ord('k'): MoveOrAttackCommand((0, -1)),
        ord('l'): MoveOrAttackCommand((1, 0)),
        ord('y'): MoveOrAttackCommand((-1, -1)),
        ord('u'): MoveOrAttackCommand((1, -1)),
        ord('b'): MoveOrAttackCommand((-1, 1)),
        ord('n'): MoveOrAttackCommand((1, 1)),
        
        # quit
        ord('Q'): GameEndCommand()
    }
    
    return commands.get(k.c)
    
    
class Command(object):
    def process(self):
        pass
    
class GameModeCommand(Command):
    pass
    
class MoveOrAttackCommand(GameModeCommand):
    def __init__(self, d):
        self.d = d
        
    def process(self, actor):
        return actor.move(self.d)
    
class GameEndCommand(GameModeCommand):
    def process(self):
        raise game.GameEndException()