from rl import globals as G
from rl.io.terminal.display.panes import pane
from rl.io import colors

class ConsolePane(pane.SinglePadPane):
    """ A (minimum) 70x3 area where game messages are printed.  Newest ones are shown first.

    example (border not rendered):
    +----------------------------------------------------------------------+
    |The goblin hits you!                                                  |
    |You hit the goblin!                                                   |
    |The goblin dies.                                                      |
    +----------------------------------------------------------------------+
    """
    min_height = 3
    min_width = 70

    def refresh(self):
        lines = G.console.get_last_lines(num_lines=self.height)

        for i, line in enumerate(lines):
            colorpair = colors.CursesColorPair(line['color'], colors.black)
            self.pad.addstr(i, 0, line['message'], colorpair.attr())