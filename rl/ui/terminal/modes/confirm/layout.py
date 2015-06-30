from termapp.term import term

from rl.ui.terminal.modes.world.layout import WorldModeLayout
from rl.ui.terminal.display.panes.console import ConfirmConsolePane

class BasicConfirmLayout(WorldModeLayout):
    """This is just like world mode layout, but with a different console"""

    # FIXME: this shouldn't need to have a world object passed to it
    # maybe layouts can be smart enough to only refresh a portion of the screen?
    def __init__(self, world, console, prompt):
        super().__init__(world, console)

        console_width = term.width
        console_height = 4
        viewport_height = min(((term.height - console_height) - 1, 80))

        console_pos = (0, viewport_height)

        self.console_pane = ConfirmConsolePane(console_width, console_height, console)
        self.panes[console_pos] = self.console_pane
