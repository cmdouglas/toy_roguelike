from termapp.term import term

from rl.ui.terminal.modes.world.layout import WorldModeLayout
from rl.ui.terminal.display.panes.log import ConfirmLogPane

class BasicConfirmLayout(WorldModeLayout):
    """This is just like world mode layout, but with a different log"""

    # FIXME: this shouldn't need to have a world object passed to it
    # maybe layouts can be smart enough to only refresh a portion of the screen?
    def __init__(self, world, prompt):
        super().__init__(world)

        log_width = term.width
        log_height = 4
        viewport_height = min(((term.height - log_height) - 1, 80))

        log_pos = (0, viewport_height)

        self.log_pane = ConfirmLogPane(log_width, log_height, world.messages)
        self.panes[log_pos] = self.log_pane
