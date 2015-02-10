import logging

logger = logging.getLogger('rl')


class Mode:
    def __init__(self):
        self.owner = None

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def newframe(self):
        pass

    def handle_keypress(self, key):
        pass

    def exit(self):
        self.owner.exit_mode(self)
