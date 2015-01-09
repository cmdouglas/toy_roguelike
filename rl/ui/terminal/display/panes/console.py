from termapp.formatstring import FormatString
from termapp.layout import Pane
from rl import globals as G


class ConsolePane(Pane):
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
        lines = G.ui.console.get_last_lines(num_lines=self.height)

        for i, line in enumerate(lines):
            self.set_line(i, FormatString().simple(line['message'], color=line['color']))