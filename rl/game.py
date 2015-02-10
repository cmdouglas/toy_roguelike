import logging

from rl.ui.terminal import TerminalUI

logger = logging.getLogger('rl')


class Game(object):
    def __init__(self, config=None):
        self.ui = TerminalUI()

    def play(self):
        self.ui.run()
        return
