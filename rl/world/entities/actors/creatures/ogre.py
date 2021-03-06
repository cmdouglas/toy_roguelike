from rl.world.entities.actors.creatures import Creature
from rl.world.ai.basic import BasicAI


class Ogre(Creature):
    type = 'ogre'
    article = "an"
    name = "ogre"
    name_plural = "ogres"
    interest_level = 18
    base_str = 12
    base_dex = 4
    base_mag = 8
    sight_radius = 8
    base_max_health = 25
    can_open_doors = True

    def __init__(self):
        super().__init__()
        self.intelligence = BasicAI(self)
