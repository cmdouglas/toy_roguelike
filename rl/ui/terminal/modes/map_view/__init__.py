import logging
from rl.ui.terminal.modes import Mode
from rl.ui.terminal.modes.map_view import commands
from rl.ui.terminal.modes.map_view import layout
from rl.ui import console
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
        self.interesting_things = self.world.board.interesting_visible_entities(
            self.world.player
        )
        self.current_ooi = 0

        if self.interesting_things:
            self.cursor_pos = self.interesting_things[self.current_ooi].tile.pos
        else:
            self.cursor_pos = self.world.player.tile.pos

        self.layout = layout.ExamineModeLayout(self)
        self.changed = True

        self.commands = {
            # movement
            ord('h'): commands.MoveCursorCommand(self, (-1, 0)),
            term.KEY_LEFT: commands.MoveCursorCommand(self, (-1, 0)),

            ord('j'): commands.MoveCursorCommand(self, (0, 1)),
            term.KEY_DOWN: commands.MoveCursorCommand(self, (0, 1)),

            ord('k'): commands.MoveCursorCommand(self, (0, -1)),
            term.KEY_UP: commands.MoveCursorCommand(self, (0, -1)),

            ord('l'): commands.MoveCursorCommand(self, (1, 0)),
            term.KEY_RIGHT: commands.MoveCursorCommand(self, (1, 0)),

            ord('y'): commands.MoveCursorCommand(self, (-1, -1)),
            ord('u'): commands.MoveCursorCommand(self, (1, -1)),
            ord('b'): commands.MoveCursorCommand(self, (-1, 1)),
            ord('n'): commands.MoveCursorCommand(self, (1, 1)),

            # Move cursor lots
            ord('H'): commands.MoveCursorCommand(self, (-8, 0)),
            ord('J'): commands.MoveCursorCommand(self, (0, 8)),
            ord('K'): commands.MoveCursorCommand(self, (0, -8)),
            ord('L'): commands.MoveCursorCommand(self, (8, 0)),
            ord('Y'): commands.MoveCursorCommand(self, (-8, -8)),
            ord('U'): commands.MoveCursorCommand(self, (8, -8)),
            ord('B'): commands.MoveCursorCommand(self, (-8, 8)),
            ord('N'): commands.MoveCursorCommand(self, (8, 8)),

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

