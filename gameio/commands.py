import config
import logging

from actions import attack
from actions import movement
from actions import wait
from actions import item

from gameio import menu

IO_MODE_GAME = 0
IO_MODE_MENU = 1

def get_user_command(game):
    keypress = None
    win = None
    if config.engine == "libtcod":
        from lib.engines.libtcod import keypress
    elif config.engine == "curses":
        from lib.engines.curses import keypress
        win = game.renderer.scr
        
    k = keypress.wait_for_keypress(win)
    
    if game.io_mode == IO_MODE_GAME:
        commands = {
            # movement
            ord('h'): MoveOrAttackCommand((-1, 0)),
            keypress.KEY_LEFT: MoveOrAttackCommand((-1, 0)),
            
            ord('j'): MoveOrAttackCommand((0, 1)),
            keypress.KEY_DOWN: MoveOrAttackCommand((0, 1)),
            
            ord('k'): MoveOrAttackCommand((0, -1)),
            keypress.KEY_UP: MoveOrAttackCommand((0, -1)),
            
            ord('l'): MoveOrAttackCommand((1, 0)),
            keypress.KEY_RIGHT: MoveOrAttackCommand((1, 0)),
            
            ord('y'): MoveOrAttackCommand((-1, -1)),
            ord('u'): MoveOrAttackCommand((1, -1)),
            ord('b'): MoveOrAttackCommand((-1, 1)),
            ord('n'): MoveOrAttackCommand((1, 1)),
            
            # wait
            ord('s'): WaitCommand(),
            
            # inventory management
            ord('g'): GetItemCommand(),
            ord(','): GetItemCommand(),
            ord('i'): ViewInventoryCommand(),
            ord('a'): UseItemCommand(),
            ord('d'): DropItemsCommand(),

            # quit
            ord('Q'): GameEndCommand()
        }
        
        if k:
            return commands.get(k.c)
        
    elif game.io_mode == IO_MODE_MENU:
        commands = {
            keypress.KEY_UP: MoveSelectedCommand(1),
            keypress.KEY_DOWN: MoveSelectedCommand(-1),
            keypress.KEY_ESC: ExitMenuCommand(),
            keypress.KEY_ENTER: SelectCommand()
            
        }
        if k:
            logging.debug(k.c)
            return commands.get(k.c)

    
    
class Command(object):
    def process(self):
        pass
    
class GameModeCommand(Command):
    pass
    
class MenuModeCommand(Command):
    pass


# game mode commands
    
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
                
                game.console.add_message('The wall is solid and unyielding.');
                game.refresh_screen()
                return None
            
            elif board[new_pos].objects['actor']:
                other = board[new_pos].objects['actor']
                return attack.AttackAction(actor, game, other)
                
        else:
            return movement.MovementAction(actor, game, self.d)
            
class ViewInventoryCommand(GameModeCommand):
    def process(self, player, game):
        game.io_mode = IO_MODE_MENU
        game.menu = menu.Menu(player.inventory, empty="You have no items.")
        game.menu_command = self
        
    def process_selected(self, game, selected):
        pass

        
class GetItemCommand(GameModeCommand):
    def process(self, player, game):
        items = player.tile.objects['items']
        
        if not items:
            return
            
        for item_ in items:
            player.queue_action(item.GetItemAction(player, game, player.tile, item_))

            
class DropItemsCommand(GameModeCommand):
    def process(self, player, game):
        pass
        
class UseItemCommand(GameModeCommand):
    def process(self, player, game):
        game.io_mode = IO_MODE_MENU
        game.menu = menu.Menu(player.inventory, empty="You have no usable items.")
        game.menu_command = self
        
    def process_selected(self, game, selected):
        if selected:
            game.player.queue_action(item.UseItemAction(game.player, game, selected))
    
class GameEndCommand(GameModeCommand):
    def process(self, player, game):
        game.exit()
        
# menu mode commands
    
class MoveSelectedCommand(MenuModeCommand):
    def __init__(self, d, n=1):
        self.d = d
        self.n = n
        
    def process(self, menu, game):
        for i in range(self.n):
            if self.d == 1:
                menu.move_up()
            else:
                menu.move_down()

class ExitMenuCommand(MenuModeCommand):
    def process(self, menu, game):
        game.io_mode = IO_MODE_GAME
        game.renderer.clear()
        game.refresh_screen()

class SelectCommand(MenuModeCommand):
    def process(self, menu, game):
        selected = menu.get_selected()
        if game.menu_command:
            game.menu_command.process_selected(game, selected)
        
        game.io_mode = IO_MODE_GAME
        game.renderer.clear()
        game.refresh_screen()
        game.menu = None
        game.menu_command = None
        

