import logging
from rl.ui.terminal.modes import Mode
from rl.ui.terminal.modes.world import mode_commands
from rl.ui.terminal.modes.world import player_commands
from rl.ui.terminal.display.layouts import gamemodelayout
from rl.ui import console
from rl.world import World, GameOver
from termapp.term import term

logger = logging.getLogger('rl')


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
        self.rendered = False

        self.player_commands = {
            # movement
            ord('h'): player_commands.MoveOrInteractCommand(self.world, (-1, 0)),
            term.KEY_LEFT: player_commands.MoveOrInteractCommand(
                self.world, (-1, 0)
            ),

            ord('j'): player_commands.MoveOrInteractCommand(self.world, (0, 1)),
            term.KEY_DOWN: player_commands.MoveOrInteractCommand(
                self.world, (0, 1)
            ),

            ord('k'): player_commands.MoveOrInteractCommand(self.world, (0, -1)),
            term.KEY_UP: player_commands.MoveOrInteractCommand(
                self.world, (0, -1)
            ),

            ord('l'): player_commands.MoveOrInteractCommand(self.world, (1, 0)),
            term.KEY_RIGHT: player_commands.MoveOrInteractCommand(
                self.world, (1, 0)
            ),

            ord('y'): player_commands.MoveOrInteractCommand(
                self.world, (-1, -1)
            ),
            ord('u'): player_commands.MoveOrInteractCommand(self.world, (1, -1)),
            ord('b'): player_commands.MoveOrInteractCommand(self.world, (-1, 1)),
            ord('n'): player_commands.MoveOrInteractCommand(self.world, (1, 1)),

            # travel
            ord('H'): player_commands.DirectionalTravelCommand(
                self.world, (-1, 0)
            ),
            ord('J'): player_commands.DirectionalTravelCommand(
                self.world, (0, 1)
            ),
            ord('K'): player_commands.DirectionalTravelCommand(
                self.world, (0, -1)
            ),
            ord('L'): player_commands.DirectionalTravelCommand(
                self.world, (1, 0)
            ),
            ord('Y'): player_commands.DirectionalTravelCommand(
                self.world, (-1, -1)
            ),
            ord('U'): player_commands.DirectionalTravelCommand(
                self.world, (1, -1)
            ),
            ord('B'): player_commands.DirectionalTravelCommand(
                self.world, (-1, 1)
            ),
            ord('N'): player_commands.DirectionalTravelCommand(
                self.world, (1, 1)
            ),

            # wait
            ord('s'): player_commands.WaitCommand(self.world),

            # inventory management
            ord('g'): player_commands.GetAllItemsCommand(self.world),
            ord(','): player_commands.GetAllItemsCommand(self.world),
        }

        self.mode_commands = {
            ord('i'): mode_commands.ViewInventoryCommand(self),
            ord('a'): mode_commands.SelectItemToUseCommand(self),
            ord('d'): mode_commands.SelectItemToDropCommand(self),

            # quit
            ord('Q'): mode_commands.ExitGameCommand(self)
        }

    def on_enter(self):
        self.rendered = False

    def on_reenter(self):
        self.rendered = False

    def next_frame(self):
        ##
        # Convoluted logic:
        #   return a frame if:
        #     - The mode has just been entered/reentered and nothing has been drawn
        #     - OR something has visibly changed
        #   return nothing if:
        #     - it's the player's turn and we're waiting for input
        #
        # TODO: refactor this.  Maybe use a generator?
        while True:
            try:
                changed = False
                events = self.world.tick()
                if events:
                    for event in events:
                        if event.perceptible(self.world.player):
                            message = event.describe(self.world.player)
                            if message:
                                self.console.add_message(message)
                            changed = True
                if changed or not self.rendered:
                    self.rendered = True
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
