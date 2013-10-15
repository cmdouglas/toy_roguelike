from gameobjects.gameobject import Actor
from gameio import console
from gameio import colors

class Mob(Actor):
    def emote(self, message, game, color=None):
        if not color:
            color = self.color
        
        if self.is_in_fov():
            name="It"
            if self.name:
                name = "The %s" % self.name
            m = "%s %s" % (name, message)
            game.console.add_message(m, color=color)
        
    def sleep_emote(self, game, color=None):
        pass
        
    def idle_emote(self, game, color=None):
        pass
        
    def describe(self):
        return "{name} ({strategy})".format(name=self.name, strategy=self.strategy.describe())
        
    