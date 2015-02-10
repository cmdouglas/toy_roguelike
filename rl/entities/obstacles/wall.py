from rl.ui import colors
from rl.ui import glyphs
from rl.entities.entity import Obstacle

class Wall(Obstacle):
    color = colors.sepia
    glyph = glyphs.medium_block
    blocks_movement=True
    blocks_vision=True
    is_wall = True
    description = 'The rough rock wall is solid and unyielding.'
    name = "rock wall"