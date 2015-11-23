import logging
from rl.util.geometry import Direction
from rl.ui import tools as ui_tools
from rl.ui.terminal.modes import Mode
from rl.ui.terminal.modes.map_view import commands
from rl.ui.terminal.modes.map_view import layout
from rl.ui import log
from termapp.term import term

logger = logging.getLogger('rl')


class ExamineMode(Mode):
    """
    This mode is entered into when the player wants to examine things.
    """

    def __init__(self, world, console):
        super().__init__()

        self.world = world
        self.console = console
        self.interesting_things = ui_tools.interesting_entities(self.world)
        self.current_ooi = 0

        if self.interesting_things:
            self.cursor_pos = self.interesting_things[self.current_ooi].tile.pos
        else:
            self.cursor_pos = self.world.player.tile.pos

        self.layout = layout.ExamineModeLayout(self)
        self.changed = True

        self.commands = {
            # movement
            ord('h'): commands.MoveCursorCommand(self, Direction.west),
            term.KEY_LEFT: commands.MoveCursorCommand(self, Direction.west),

            ord('j'): commands.MoveCursorCommand(self, Direction.south),
            term.KEY_DOWN: commands.MoveCursorCommand(self, Direction.south),

            ord('k'): commands.MoveCursorCommand(self, Direction.north),
            term.KEY_UP: commands.MoveCursorCommand(self, Direction.north),

            ord('l'): commands.MoveCursorCommand(self, Direction.east),
            term.KEY_RIGHT: commands.MoveCursorCommand(self, Direction.east),

            ord('y'): commands.MoveCursorCommand(self, Direction.northwest),
            ord('u'): commands.MoveCursorCommand(self, Direction.northeast),
            ord('b'): commands.MoveCursorCommand(self, Direction.southwest),
            ord('n'): commands.MoveCursorCommand(self, Direction.southeast),

            # Move cursor lots
            ord('H'): commands.MoveCursorCommand(
                self, Direction.west, repeat=8
            ),
            ord('J'): commands.MoveCursorCommand(
                self, Direction.south, repeat=8
            ),
            ord('K'): commands.MoveCursorCommand(
                self, Direction.north, repeat=8
            ),
            ord('L'): commands.MoveCursorCommand(
                self, Direction.east, repeat=8
            ),
            ord('Y'): commands.MoveCursorCommand(
                self, Direction.northwest, repeat=8
            ),
            ord('U'): commands.MoveCursorCommand(
                self, Direction.northeast, repeat=8
            ),
            ord('B'): commands.MoveCursorCommand(
                self, Direction.southwest, repeat=8
            ),
            ord('N'): commands.MoveCursorCommand(
                self, Direction.southeast, repeat=8
            ),

            # go to point
            ord('.'): commands.GoToPointCommand(self),
            ord('g'): commands.GoToPointCommand(self),

            term.KEY_ESCAPE: commands.ExitModeCommand(self),
            term.KEY_ENTER:  commands.ExitModeCommand(self),
            ord(' '): commands.ExitModeCommand(self),

            term.KEY_TAB: commands.JumpToNextInterestingThingCommand(self),
            term.KEY_BTAB: commands.JumpToPreviousInterestingThingCommand(self)
        }

    def previous_interesting_thing(self):
        self.current_ooi -= 1
        if self.current_ooi < 0:
            self.current_ooi = len(self.interesting_things) -1

        return self.interesting_things[self.current_ooi]

    def next_interesting_thing(self):
        self.current_ooi += 1
        if len(self.interesting_things) <= self.current_ooi:
            self.current_ooi = 0

        return self.interesting_things[self.current_ooi]

    def next_frame(self):
        if self.changed:
            self.changed = False
            return self.layout.render()

    def handle_keypress(self, key):
        if key.is_sequence:
            code = key.code

        else:
            code = ord(str(key))

        # these commands are executed on the current mode
        if code in self.commands:
            command = self.commands[code]
            command.process()

