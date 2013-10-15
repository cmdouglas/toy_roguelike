from gameio import colors
from gameobjects.gameobject import Obstacle

class Wall(Obstacle):
    color = colors.sepia
    char = '#'
    blocks_movement=True
    blocks_vision=True
        