import random
from rl.ui import colors
from rl.entities.actors.creature import Creature
from rl.ai.basic import BasicAI


class Ogre(Creature):
    article = "an"
    name = u"ogre"
    name_plural = "ogres"
    interest_level = 18
    color = colors.bright_red
    glyph = 'O'
    sight_radius = 8
    max_health = 25
    can_open_doors = True

    def __init__(self):
        self.health = self.max_health
        self.intelligence = BasicAI(self)
        self.str = 10
