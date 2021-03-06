import textwrap
from rl.ui.terminal.display import colors
from termapp.formatstring import FormatString
from termapp.layout import Pane


class LogPane(Pane):
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

    def __init__(self, width, height, log):
        super().__init__(width, height)
        self.log = log

    def refresh(self):
        lines = self.get_lines(self.height)

        for i, line in enumerate(lines):
            self.set_line(i, FormatString(line))

    def get_lines(self, num_lines):
        messages = self.log[-num_lines:]
        lines = []
        for message in messages:
            new_lines = textwrap.wrap(message, self.width)
            lines.extend(new_lines)

        return lines[-num_lines:]


class ConfirmLogPane(LogPane):
    """
    Like a log pane, but askes for --MORE--, or maybe Continue? (Y/N)
    """

    def __init__(self, width, height, log, prompt='--MORE--'):
        super().__init__(width, height, log)
        self.prompt = prompt

    def refresh(self):
        lines = self.get_lines(self.height)

        for i, line in enumerate(lines):
            self.set_line(i, FormatString(line))

        self.set_line(self.height - 1, FormatString().simple(self.prompt, color=colors.bright_white))