from rl.world.entities import Entity

class Actor(Entity):
    blocks_movement = True
    can_act = True
    can_open_doors = False
    is_player = False

    def on_move(self, old_pos, new_pos):
        pass

    def process_turn(self, world):
        return False

    def can_see_point(self, point):
        return False

#
# def dump_actor(actor):
#     return dict(
#         _save_id=id(actor)
#     )
#
# def load_actor(data, actor):
#     actor._save_id = data['_save_id']