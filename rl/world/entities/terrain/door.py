from rl.world.entities import terrain
from rl.world.actions import interact


class ClosedDoor(terrain.Terrain):
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


class OpenDoor(terrain.Terrain):
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
