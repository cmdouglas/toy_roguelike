import config
import logging
import game

from actions import attack
from actions import movement
from actions import wait

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
        
        # wait
        ord('s'): WaitCommand(),
        
        # quit
        ord('Q'): GameEndCommand()
    }
    
    if k:
        return commands.get(k.c)
    
    
class Command(object):
    def process(self):
        pass
    
class GameModeCommand(Command):
    pass
    
class WaitCommand(GameModeCommand):
    def process(self, actor, game):
        return wait.WaitAction(actor, game)
    
class MoveOrAttackCommand(GameModeCommand):
    def __init__(self, d):
        self.d = d
        
    def process(self, actor, game):
        
        board = game.board
        x, y = actor.tile.pos
        dx, dy = self.d
        new_pos = (x+dx, y+dy)
        
        if board.position_is_valid(new_pos) and board[new_pos].blocks_movement():
            if board[new_pos].objects['obstacle']:
                game.console.add_message('You bump into the wall.');
                return wait.WaitAction(actor, game)
            
            elif board[new_pos].objects['actor']:
                other = board[new_pos].objects['actor']
                return attack.AttackAction(actor, game, other)
                
        else:
            return movement.MovementAction(actor, game, self.d)
    
class GameEndCommand(GameModeCommand):
    def process(self):
        raise game.GameEndException()