class Intelligence:
    def __init__(self, actor):
        self.actor = actor
        self._strategy = None

    @property
    def strategy(self):
        return self._strategy

    @property
    def board(self):
        return self.actor.tile.board

    @property
    def world(self):
        return self.board.world

    @strategy.setter
    def strategy(self, strategy):
        if self._strategy:
            self._strategy.intelligence = None

        self._strategy = strategy
