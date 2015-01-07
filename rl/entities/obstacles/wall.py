from rl.ui import colors
from rl.ui import chars
from rl.entities.entity import Obstacle

class Wall(Obstacle):
    color = colors.sepia
    char = chars.medium_block
    blocks_movement=True
    blocks_vision=True
    is_wall = True
    description = 'The rough rock wall is solid and unyielding.'