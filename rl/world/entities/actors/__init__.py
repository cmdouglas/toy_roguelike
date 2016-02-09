from rl.world.entities import Entity

class Actor(Entity):
    blocks_movement = True
    can_open_doors = False
    is_player = False

    def on_move(self, old_pos, new_pos):
        pass

    def process_turn(self, world):
        return False

    def can_see_point(self, point):
        return False

    def __getstate__(self):
        state = super().__getstate__()
        state.update(dict(
            _save_id=id(self)
        ))

        return state

    def __setstate__(self, state):
        self._save_id = state['save_id']
