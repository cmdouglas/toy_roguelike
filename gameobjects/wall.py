from gameio import colors
from gameio import chars
from gameobjects.gameobject import Obstacle

class Wall(Obstacle):
    color = colors.sepia
    char = chars.medium_block
    blocks_movement=True
    blocks_vision=True
        