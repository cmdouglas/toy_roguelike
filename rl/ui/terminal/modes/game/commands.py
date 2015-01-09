import logging

from rl import globals as G
from rl.ui import commands
from rl.ui.terminal.modes import menu
from rl.actions import interact
from rl.actions import movement
from rl.actions import travel
from rl.actions import wait
from rl.actions import item

def get_user_command(keypress):
    term = G.ui.term
    commands = {
        # movement
        ord('h'): MoveOrInteractCommand((-1, 0)),
        term.KEY_LEFT: MoveOrInteractCommand((-1, 0)),

        ord('j'): MoveOrInteractCommand((0, 1)),
        term.KEY_DOWN: MoveOrInteractCommand((0, 1)),

        ord('k'): MoveOrInteractCommand((0, -1)),
        term.KEY_UP: MoveOrInteractCommand((0, -1)),

        ord('l'): MoveOrInteractCommand((1, 0)),
        term.KEY_RIGHT: MoveOrInteractCommand((1, 0)),

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
        ord('g'): GetAllItemsCommand(),
        ord(','): GetAllItemsCommand(),
        ord('i'): ViewInventoryCommand(),
        ord('a'): SelectItemToUseCommand(),
        ord('d'): DropItemsCommand(),

        # quit
        ord('Q'): ExitGameCommand()
    }

    if keypress.is_sequence:
        code = keypress.code

    else:
        code = ord(str(keypress))

    return commands.get(code)


class GameModeCommand(commands.Command):
    pass


class PlayerCommand(GameModeCommand):
    """A command that is passed on to the player"""
    pass

# game mode commands
class WaitCommand(PlayerCommand):
    def process(self, actor):
        return wait.WaitAction(actor)


class MoveOrInteractCommand(PlayerCommand):
    def __init__(self, d):
        self.d = d

    def process(self, actor):
        board = G.world.board
        x, y = actor.tile.pos
        dx, dy = self.d
        new_pos = (x+dx, y+dy)

        if board.position_is_valid(new_pos) and board[new_pos].blocks_movement():
            if board[new_pos].entities['obstacle']:
                ob = board[new_pos].entities['obstacle']
                return ob.default_interaction(actor)


            elif board[new_pos].entities['actor']:
                other = board[new_pos].entities['actor']
                return interact.AttackAction(actor, other)

        else:
            return movement.MovementAction(actor, self.d)


class DirectionalTravelCommand(PlayerCommand):
    def __init__(self, d):
        self.d = d

    def process(self, actor):
        return travel.DirectionalTravelAction(actor, self.d)


class GetAllItemsCommand(PlayerCommand):
    def process(self, player):
        items = player.tile.entities['items']

        if not items:
            return

        for item_ in items:
            player.intelligence.add_command(GetItemCommand(item_))

class GetItemCommand(PlayerCommand):
    def __init__(self, item):
        self.item = item

    def process(self, player):
        return item.GetItemAction(player, player.tile, self.item)


class UseItemCommand(PlayerCommand):
    def __init__(self, item):
        self.item=item

    def process(self, player):
        return item.UseItemAction(G.world.player, self.item)


class DropItemsCommand(PlayerCommand):
    def process(self, player):
        pass


##
# these affect the ui mode of the game (bring up menus, etc)

class SelectItemToUseCommand(GameModeCommand):
    def process(self, mode):
        player = G.world.player

        def on_select(item):
            player.intelligence.add_command(UseItemCommand(item))

        items = G.world.player.inventory
        mode.enter_child_mode(
            menu.SingleSelectMenuMode(
                items,
                empty="You have no items.",
                selected_callback=on_select
            )
        )

class ViewInventoryCommand(GameModeCommand):
    def process(self, mode):
        items = G.world.player.inventory
        mode.enter_child_mode(
            menu.SingleSelectMenuMode(
                items,
                empty="You have no items."
            )
        )

class ExitGameCommand(GameModeCommand):
    def process(self, mode):
        mode.exit()