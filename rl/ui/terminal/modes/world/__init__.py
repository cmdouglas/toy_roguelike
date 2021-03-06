import logging

from rl.ui import debug_commands
from rl.ui import player_commands
from rl.ui.player_commands import item as item_commands
from rl.ui.player_commands import travel as travel_commands
from rl.ui.terminal import modes
from rl.ui.terminal.modes.confirm import SimpleConfirmMode
from rl.ui.terminal.modes.world import layout
from rl.ui.terminal.modes.world import mode_commands
from rl.ui.terminal.modes.prompt import PromptMode
from rl.util.geometry import Direction
from rl.save import delete_save
from termapp.term import term

logger = logging.getLogger('rl')


class WorldMode(modes.Mode):
    """
    This mode owns the game world, and processes most of the commands that
    affect it.  It displays a viewport of the world, and a HUD for the player
    that consists of basic stats, things the player can see, and  a log
    of events.
    """

    def __init__(self, world):
        super().__init__()

        self.world = world

        self.layout = layout.WorldModeLayout(self.world)
        self.rendered = False
        self.is_game_over = False

        self.player_commands = {
            # movement
            ord('h'): player_commands.MoveOrInteractCommand(
                self.world.player, Direction.west
            ),
            term.KEY_LEFT: player_commands.MoveOrInteractCommand(
                self.world.player, Direction.west
            ),

            ord('j'): player_commands.MoveOrInteractCommand(
                self.world.player, Direction.south
            ),
            term.KEY_DOWN: player_commands.MoveOrInteractCommand(
                self.world.player, Direction.south
            ),

            ord('k'): player_commands.MoveOrInteractCommand(
                self.world.player, Direction.north
            ),
            term.KEY_UP: player_commands.MoveOrInteractCommand(
                self.world.player, Direction.north
            ),

            ord('l'): player_commands.MoveOrInteractCommand(
                self.world.player, Direction.east
            ),
            term.KEY_RIGHT: player_commands.MoveOrInteractCommand(
                self.world.player, Direction.east
            ),

            ord('y'): player_commands.MoveOrInteractCommand(
                self.world.player, Direction.northwest
            ),
            ord('u'): player_commands.MoveOrInteractCommand(
                self.world.player, Direction.northeast)
            ,
            ord('b'): player_commands.MoveOrInteractCommand(
                self.world.player, Direction.southwest
            ),
            ord('n'): player_commands.MoveOrInteractCommand(
                self.world.player, Direction.southeast
            ),

            # travel
            ord('H'): travel_commands.DirectionalTravelCommand(
                self.world.player, Direction.west
            ),
            ord('J'): travel_commands.DirectionalTravelCommand(
                self.world.player, Direction.south
            ),
            ord('K'): travel_commands.DirectionalTravelCommand(
                self.world.player, Direction.north
            ),
            ord('L'): travel_commands.DirectionalTravelCommand(
                self.world.player, Direction.east
            ),
            ord('Y'): travel_commands.DirectionalTravelCommand(
                self.world.player, Direction.northwest
            ),
            ord('U'): travel_commands.DirectionalTravelCommand(
                self.world.player, Direction.northeast
            ),
            ord('B'): travel_commands.DirectionalTravelCommand(
                self.world.player, Direction.southwest
            ),
            ord('N'): travel_commands.DirectionalTravelCommand(
                self.world.player, Direction.southeast
            ),

            # wait
            ord('s'): player_commands.WaitCommand(self.world.player),
            ord('.'): player_commands.WaitCommand(self.world.player),

            # inventory management
            ord('g'): item_commands.GetAllItemsCommand(self.world.player),
            ord(','): item_commands.GetAllItemsCommand(self.world.player),

        }

        self.mode_commands = {
            ord('i'): mode_commands.ViewInventoryCommand(self),
            ord('a'): mode_commands.SelectItemToUseCommand(self),
            ord('d'): mode_commands.SelectItemToDropCommand(self),
            ord('x'): mode_commands.ExamineCommand(self),

            # save
            ord('S'): mode_commands.SaveGameCommand(self),

            # quit
            ord('Q'): mode_commands.ExitGameCommand(self),

            # debug
            ord('M'): debug_commands.RevealMapCommand(self)
        }

    def on_enter(self):
        self.rendered = False

    def on_reenter(self):
        self.rendered = False

    def next_frame(self):

        while True:
            # is the player dead?  make the player confirm and then exit if so.
            if not self.world.player.is_alive:
                if not self.is_game_over:
                    self.game_over()
                return

            redraw_screen = self.world.tick()
            if redraw_screen or not self.rendered:
                self.rendered = True
                return self.layout.render()

            if self.world.current_actor == self.world.player:
                return

    def confirm(self, callback, prompt="--MORE--"):
        self.owner.enter_mode(SimpleConfirmMode(
            self.world, prompt, callback
        ))

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

    def game_over(self):
        self.is_game_over = True

        def _do_game_over():
            if self.world.save_filename:
                delete_save(self.world.save_filename)
            self.exit()

        self.confirm(_do_game_over)

    def name_player(self):
        def on_entry(text):
            self.world.player.name = text

        self.owner.enter_mode(PromptMode(
            prompt="What is your name",
            max_length = "16",
            on_entry=on_entry
        ))

    def force_redraw(self):
        self.rendered = False
