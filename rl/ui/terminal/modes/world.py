from rl.ui.terminal.modes import Mode
from rl.ui.terminal.modes import menu
from rl.ui.terminal.display.layouts import gamemodelayout
from rl.ui import console
from rl.ai import playercommand
from rl.world import World, GameOver
from termapp.term import term

class WorldMode(Mode):
    """
    This mode owns the game world, and processes most of the commands that
    affect it.  It displays a viewport of the world, and a HUD for the player
    that consists of basic stats, things the player can see, and  a log
    of events.
    """

    def __init__(self, world=None):
        super().__init__()

        if world:
            self.world = world

        else:
            self.world = World()

        self.console = console.Console()
        self.layout = gamemodelayout.GameModeLayout(self.world, self.console)

        self.player_commands = {
            # movement
            ord('h'): playercommand.MoveOrInteractCommand(self.world, (-1, 0)),
            term.KEY_LEFT: playercommand.MoveOrInteractCommand(
                self.world, (-1, 0)
            ),

            ord('j'): playercommand.MoveOrInteractCommand(self.world, (0, 1)),
            term.KEY_DOWN: playercommand.MoveOrInteractCommand(
                self.world, (0, 1)
            ),

            ord('k'): playercommand.MoveOrInteractCommand(self.world, (0, -1)),
            term.KEY_UP: playercommand.MoveOrInteractCommand(
                self.world, (0, -1)
            ),

            ord('l'): playercommand.MoveOrInteractCommand(self.world, (1, 0)),
            term.KEY_RIGHT: playercommand.MoveOrInteractCommand(
                self.world, (1, 0)
            ),

            ord('y'): playercommand.MoveOrInteractCommand(
                self.world, (-1, -1)
            ),
            ord('u'): playercommand.MoveOrInteractCommand(self.world, (1, -1)),
            ord('b'): playercommand.MoveOrInteractCommand(self.world, (-1, 1)),
            ord('n'): playercommand.MoveOrInteractCommand(self.world, (1, 1)),

            # travel
            ord('H'): playercommand.DirectionalTravelCommand(
                self.world, (-1, 0)
            ),
            ord('J'): playercommand.DirectionalTravelCommand(
                self.world, (0, 1)
            ),
            ord('K'): playercommand.DirectionalTravelCommand(
                self.world, (0, -1)
            ),
            ord('L'): playercommand.DirectionalTravelCommand(
                self.world, (1, 0)
            ),
            ord('Y'): playercommand.DirectionalTravelCommand(
                self.world, (-1, -1)
            ),
            ord('U'): playercommand.DirectionalTravelCommand(
                self.world, (1, -1)
            ),
            ord('B'): playercommand.DirectionalTravelCommand(
                self.world, (-1, 1)
            ),
            ord('N'): playercommand.DirectionalTravelCommand(
                self.world, (1, 1)
            ),

            # wait
            ord('s'): playercommand.WaitCommand(self.world),

            # inventory management
            ord('g'): playercommand.GetAllItemsCommand(self.world),
            ord(','): playercommand.GetAllItemsCommand(self.world),
        }

        self.mode_commands = {
            ord('i'): ViewInventoryCommand(self),
            ord('a'): SelectItemToUseCommand(self),
            ord('d'): SelectItemToDropCommand(self),

            # quit
            ord('Q'): ExitGameCommand(self)
        }

    def newframe(self):
        ##
        # Convoluted logic:  return a frame if something visibly changed in the
        # world.  return nothing if it's the player's turn but nothing's
        # changed.
        #
        # TODO: refactor this.  Maybe use a generator?
        while True:
            try:
                events = self.world.tick()
                if events:
                    changed = False
                    for event in events:
                        if event.perceptible(self.world.player):
                            self.console.add_message(event.describe(self.world.player))
                            changed = True

                    return self.layout.render()

                if self.world.current_actor == self.world.player:
                    return

            except(GameOver):
                self.exit()

    def handle_keypress(self, key):
        if key.is_sequence:
            code = key.code

        else:
            code = ord(str(key))

        # these commands are passed to the player
        if code in self.player_commands:
            command = self.player_commands[code]
            self.world.player.intelligence.add_command(command)

        # these commands are executed on the current mode
        elif code in self.mode_commands:
            command = self.mode_commands[code]
            command.process()


class GameModeCommand:
    def __init__(self, mode):
        self.mode = mode


class SelectItemToUseCommand(GameModeCommand):
    def process(self):
        player = self.mode.world.player

        def on_select(item):
            player.intelligence.add_command(
                playercommand.UseItemCommand(self.mode.world, item)
            )

        items = self.mode.world.player.inventory
        self.mode.owner.enter_mode(
            menu.SingleSelectMenuMode(
                items.to_dict(),
                empty="You have no items.",
                selected_callback=on_select
            )
        )


class ViewInventoryCommand(GameModeCommand):
    def process(self):
        items = self.mode.world.player.inventory
        self.mode.owner.enter_mode(
            menu.SingleSelectMenuMode(
                items.to_dict(),
                empty="You have no items."
            )
        )


class SelectItemToDropCommand(GameModeCommand):
    def process(self):
        player = self.mode.world.player

        def on_select(item):
            player.intelligence.add_command(
                playercommand.DropItemCommand(self.mode.world, item)
            )

        items = self.mode.world.player.inventory
        self.mode.owner.enter_mode(
            menu.SingleSelectMenuMode(
                items.to_dict(),
                empty="You have no items.",
                selected_callback=on_select
            )
        )


class ExitGameCommand(GameModeCommand):
    def process(self):
        self.mode.exit()
