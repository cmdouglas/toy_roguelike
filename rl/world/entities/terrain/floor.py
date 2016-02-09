from rl.world.entities.terrain import Terrain


class Floor(Terrain):
    blocks_movement = False
    blocks_vision = False
