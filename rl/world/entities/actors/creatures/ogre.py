#from rl.world.save import rl_types
from rl.ui import colors
from rl.world.entities.actors.creatures import Creature
from rl.world.ai.basic import BasicAI


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

#
# @rl_types.dumper(Ogre, 'ogre', 1)
# def _dump_ogre(ogre):
#     return dump_creature(ogre)
#
#
# @rl_types.loader('ogre', 1)
# def _load_goblin(data, version):
#     ogre = Ogre()
#     load_creature(data, ogre)
#     return ogre
