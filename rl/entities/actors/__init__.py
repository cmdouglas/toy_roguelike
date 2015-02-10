from rl.entities import entity

class Actor(entity.Entity):
    blocks_movement = True
    can_act = True
    can_open_doors = False
    is_player = False

    def on_move(self, old_pos, new_pos):
        pass

    def process_turn(self, world):
        return False

    def can_see(self, point, board):
        return False

