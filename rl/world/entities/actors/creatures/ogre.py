from rl.world.entities.actors.creatures import Creature
from rl.world.ai.basic import BasicAI


class Ogre(Creature):
    article = "an"
    name = u"ogre"
    name_plural = "ogres"
    interest_level = 18
    base_str = 8
    sight_radius = 8
    base_max_health = 25
    can_open_doors = True

    def __init__(self):
        super().__init__()
        self.intelligence = BasicAI(self)
