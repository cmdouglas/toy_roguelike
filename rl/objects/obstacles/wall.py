from rl.io import colors
from rl.io import chars
from rl.objects.gameobject import Obstacle

class Wall(Obstacle):
    color = colors.sepia
    char = chars.medium_block
    blocks_movement=True
    blocks_vision=True
    is_wall = True
    description = 'The rough rock wall is solid and unyielding.'