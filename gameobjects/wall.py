import libtcodpy as libtcod

from gameobjects.base import Obstacle

class Wall(Obstacle):
    color = libtcod.sepia
    char = '#'
    blocks_movement=True
    blocks_vision=True
        