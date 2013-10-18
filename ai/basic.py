from ai.strategies import idle, aggressive
from ai import primitives

class BasicAI(object):
    def __init__(self, actor):
        
        self.actor = actor
        self.strategy = idle.IdleStrategy()
        
    def do_ai(self, game):
        if primitives.can_see(self.actor, game.player, game.board):
            self.strategy = aggressive.AggressiveStrategy()
        
        else:
            self.strategy = idle.IdleStrategy()
        
        r = self.strategy.do_strategy(self.actor, game, [])
        
        return r['action']