from gameobjects.base import Actor
from ai import primitives
from io import console
from io import colors

class Mob(Actor):
    def emote(self, message, game, color=None):
        if not color:
            color = self.color
        
        name="It"
        if self.name:
            name = "The %s" % self.name
        if primitives.can_see_player(self, game.board):
            m = "%s %s" % (name, message)
            game.console.add_message(m, color=color)
        
    def sleep_emote(self, game, color=None):
        pass
        
    def idle_emote(self, game, color=None):
        pass
        
    