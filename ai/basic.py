import logging
from ai.strategies import idle

class BasicAI(object):
    def __init__(self, actor):
        
        self.actor = actor
        self.strategy = idle.IdleStrategy()
        
    def do_ai(self, game):
        r = self.strategy.do_strategy(self.actor, game, [])
        return r['action']