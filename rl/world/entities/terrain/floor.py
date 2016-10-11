from rl.world.entities import terrain


class Floor(terrain.Terrain):
    type = 'floor'
    article = 'the'
    name = 'floor'
    blocks_movement = False
    blocks_vision = False
