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
    base_str = 8
    sight_radius = 8
    base_max_health = 25
    can_open_doors = True

    def __init__(self):
        super().__init__()
        self.intelligence = BasicAI(self)
