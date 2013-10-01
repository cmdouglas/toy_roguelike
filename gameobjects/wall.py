from io import colors
from gameobjects.base import Obstacle

class Wall(Obstacle):
    color = colors.sepia
    char = '#'
    blocks_movement=True
    blocks_vision=True
        