import logging
from termapp.application import StopApplication

logger = logging.getLogger('rl')


class Mode:
    def __init__(self):
        self.child_mode = None
        self.parent_mode = None

    def enter_child_mode(self, mode):
        logger.debug("Entering child mode: {}".format(repr(mode)))
        self.child_mode = mode
        mode.parent_mode = self

    def newframe(self):
        pass

    def handle_keypress(self, key):
        pass

    def exit(self):
        logger.debug("Exiting Mode {}".format(repr(self)))

        if self.parent_mode:
            self.parent_mode.child_mode = None
            self.parent_mode = None

        else:
            # if we're the top level mode, then kill the app
            raise StopApplication
