import enum

class ModeSignal(enum.Enum):
    MODE_EXIT = 0

class Mode(object):
    def __init__(self, parent=None, data=None):
        self.parent = parent

        if data is None:
            data = {}

        self.data = data

    def process(self):
        pass