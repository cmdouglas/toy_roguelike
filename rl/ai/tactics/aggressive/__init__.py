from rl.ai.tactics import Tactics

class AggressiveTactics(Tactics):
    @property
    def target(self):
        return self.strategy.target

    @property
    def target_last_seen(self):
        return self.strategy.target_last_seen