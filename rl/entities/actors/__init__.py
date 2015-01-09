from rl import globals as G
from rl.entities import entity

class Actor(entity.Entity):
    blocks_movement = True
    can_act = True
    can_open_doors = False

    def on_move(self, old_pos, new_pos):
        pass

    def process_turn(self):
        return False

    def on_spawn(self):
        G.world.update()

    def on_despawn(self):
        G.world.update()