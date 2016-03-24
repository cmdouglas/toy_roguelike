from rl.world.entities.terrain import Terrain


class Floor(Terrain):
    type = 'floor'
    blocks_movement = False
    blocks_vision = False
