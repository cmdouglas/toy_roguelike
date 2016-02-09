CONTINUE = 0
COMPLETE = 1
INTERRUPTED = 2


class Strategy(object):
    def __init__(self, intelligence):
        self.intelligence = intelligence
        self._tactics = None

    def do_strategy(self):
        pass

    def describe(self):
        return ""

    @property
    def tactics(self):
        return self._tactics

    @property
    def actor(self):
        return self.intelligence.actor

    @property
    def board(self):
        return self.actor.tile.board

    @property
    def world(self):
        return self.board.world

    @tactics.setter
    def tactics(self, tactics):
        if self._tactics:
            self._tactics.strategy = None

        self._tactics = tactics

    def __getstate__(self):
        return dict(
            tactics=self._tactics
        )

    def __setstate__(self, state):
        self.tactics = state['tactics']
