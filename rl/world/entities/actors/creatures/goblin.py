from rl.world.entities.actors.creatures import Creature
from rl.world.ai.basic import BasicAI


class Goblin(Creature):
    name = "goblin"
    name_plural = "goblins"
    interest_level = 10
    sight_radius = 8
    base_str = 4
    base_max_health = 10
    can_open_doors = True

    def __init__(self):
        super().__init__()
        self.intelligence = BasicAI(self)
