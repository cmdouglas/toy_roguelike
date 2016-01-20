from rl.ui import colors
from rl.ui import glyphs
from rl.world.entities.terrain import Terrain
#from rl.world.save import rl_types

class Wall(Terrain):
    color = colors.sepia
    glyph = glyphs.medium_block
    blocks_movement=True
    blocks_vision=True
    is_wall = True
    description = 'The rough rock wall is solid and unyielding.'
    name = "rock wall"
    name_plural = "rock walls"
#
# @rl_types.dumper(Wall, 'wall', 1)
# def _dump_wall(wall):
#     return "#"
#
# @rl_types.loader('wall', 1)
# def _load_wall(data, version):
#     return Wall()