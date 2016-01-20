import logging

logger = logging.getLogger('rl')

from termapp.term import term

from rl.ui.terminal.modes import Mode
from rl.ui.terminal.modes.confirm.layout import BasicConfirmLayout

class SimpleConfirmMode(Mode):
    """Displays world mode like normal, but asks for --MORE--
    Accepts <space>, <enter>, and <escape> to continue.
    """
    def __init__(self, world, log, prompt, callback):
        super().__init__()

        self.world = world
        self.prompt = prompt
        self.callback = callback
        self.log = log
        self.layout = BasicConfirmLayout(self.world, self.log, self.prompt)

        self.changed = True

    def next_frame(self):
        if self.changed:
            self.changed = False
            return self.layout.render()

    def handle_keypress(self, key):
        if key.is_sequence:
            letter = None
            code = key.code

        else:
            letter = str(key)
            code = ord(letter)

        if letter == ' ' or code in [term.KEY_ENTER, term.KEY_ESCAPE]:
            self.exit()

    def on_exit(self):
        self.callback()


