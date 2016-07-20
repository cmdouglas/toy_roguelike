from rl.world.entities.terrain import Terrain


class Floor(Terrain):
    type = 'floor'
    article = 'the'
    name = 'floor'
    blocks_movement = False
    blocks_vision = False
