from rl.ui import colors
#from rl.world.save import rl_types
from rl.world.entities.actors.creature import Creature
from rl.world.ai.basic import BasicAI


class Goblin(Creature):
    name = "goblin"
    name_plural = "goblins"
    interest_level = 10
    color = colors.green
    glyph = 'g'
    sight_radius = 8
    base_str = 4
    base_max_health = 10
    can_open_doors = True

    def __init__(self):
        super().__init__()
        self.intelligence = BasicAI(self)

#
# @rl_types.dumper(Goblin, 'goblin', 1)
# def _dump_goblin(goblin):
#     return dump_creature(goblin)
#
#
# @rl_types.loader('goblin', 1)
# def _load_goblin(data, version):
#     goblin = Goblin()
#     load_creature(data, goblin)
#     return goblin