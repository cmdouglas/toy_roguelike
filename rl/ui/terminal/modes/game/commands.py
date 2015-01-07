import logging

from rl import globals as G
from rl.ui import commands
from rl.ui.lib.engines.curses import keypress
from rl.modes import mode
from rl.modes import menumode
from rl.actions import interact
from rl.actions import movement
from rl.actions import travel
from rl.actions import wait
from rl.actions import item

def get_user_command():
    k = keypress.wait_for_keypress()
    commands = {
        # movement
        ord('h'): MoveOrInteractCommand((-1, 0)),
        keypress.KEY_LEFT: MoveOrInteractCommand((-1, 0)),

        ord('j'): MoveOrInteractCommand((0, 1)),
        keypress.KEY_DOWN: MoveOrInteractCommand((0, 1)),

        ord('k'): MoveOrInteractCommand((0, -1)),
        keypress.KEY_UP: MoveOrInteractCommand((0, -1)),

        ord('l'): MoveOrInteractCommand((1, 0)),
        keypress.KEY_RIGHT: MoveOrInteractCommand((1, 0)),

        ord('y'): MoveOrInteractCommand((-1, -1)),
        ord('u'): MoveOrInteractCommand((1, -1)),
        ord('b'): MoveOrInteractCommand((-1, 1)),
        ord('n'): MoveOrInteractCommand((1, 1)),

        # travel
        ord('H'): DirectionalTravelCommand((-1, 0)),
        ord('J'): DirectionalTravelCommand((0, 1)),
        ord('K'): DirectionalTravelCommand((0, -1)),
        ord('L'): DirectionalTravelCommand((1, 0)),
        ord('Y'): DirectionalTravelCommand((-1, -1)),
        ord('U'): DirectionalTravelCommand((1, -1)),
        ord('B'): DirectionalTravelCommand((-1, 1)),
        ord('N'): DirectionalTravelCommand((1, 1)),

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

class GameModeCommand(commands.Command):
    pass

# game mode commands

class WaitCommand(GameModeCommand):
    def process(self, actor):
        return wait.WaitAction(actor)

class MoveOrInteractCommand(GameModeCommand):
    def __init__(self, d):
        self.d = d

    def process(self, actor):
        board = G.board
        x, y = actor.tile.pos
        dx, dy = self.d
        new_pos = (x+dx, y+dy)

        if board.position_is_valid(new_pos) and board[new_pos].blocks_movement():
            if board[new_pos].objects['obstacle']:
                ob = board[new_pos].objects['obstacle']
                return ob.default_interaction(actor)


            elif board[new_pos].objects['actor']:
                other = board[new_pos].objects['actor']
                return interact.AttackAction(actor, other)

        else:
            return movement.MovementAction(actor, self.d)

class DirectionalTravelCommand(GameModeCommand):
    def __init__(self, d):
        self.d = d

    def process(self, actor):
        return travel.DirectionalTravelAction(actor, self.d)


class ViewInventoryCommand(GameModeCommand):
    def process(self, player):
        m = menumode.ViewInventoryMode()
        return m.process()

class GetItemCommand(GameModeCommand):
    def process(self, player):
        items = player.tile.objects['items']

        if not items:
            return

        for item_ in items:
            player.queue_action(item.GetItemAction(player, player.tile, item_))


class DropItemsCommand(GameModeCommand):
    def process(self, player):
        pass

class UseItemCommand(GameModeCommand):
    def process(self, player):
        m = menumode.UseItemMode()
        selected = m.process()

        if selected:
            return item.UseItemAction(G.player, selected)

class GameEndCommand(GameModeCommand):
    def process(self, player):
        raise mode.ModeExitException()

