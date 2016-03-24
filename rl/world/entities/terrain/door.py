from rl.world.entities.terrain import Terrain
from rl.world.actions import interact


class ClosedDoor(Terrain):
    type = 'closed_door'
    blocks_movement = True
    blocks_vision = True
    is_door = True
    description = "The heavy wooden door is solidly closed."
    name = "door"
    name_plural = "doors"
    artificial = True

    def open(self):
        self.tile.terrain = OpenDoor()

    def default_interaction(self, actor):
        return interact.OpenAction(actor, self)

    def on_first_seen(self):
        surrounding_terrain = [t.terrain for t in self.tile.neighbors() if t.terrain.blocks_movement]
        for terrain in surrounding_terrain:
            terrain.should_update = True


class OpenDoor(Terrain):
    type = 'open_door'
    blocks_movement = False
    blocks_vision = False
    is_door = True
    description = "The heavy wooden door stands open."
    name = "door"
    name_plural = "doors"
    artificial = True

    def close(self):
        self.tile.terrain = ClosedDoor()

    def default_interaction(self, actor):
        return interact.CloseAction(actor, self)

    def on_first_seen(self):
        surrounding_terrain = [t.terrain for t in self.tile.neighbors() if t.terrain.blocks_movement]
        for terrain in surrounding_terrain:
            terrain.should_update = True