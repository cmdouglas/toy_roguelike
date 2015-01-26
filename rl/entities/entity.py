from rl.ui import colors
from rl.actions import interact


class Entity(object):
    color = colors.light_gray
    bgcolor = None
    glyph = ' '
    blocks_movement = False
    blocks_vision = False
    can_act = False
    can_be_taken = False
    interest_level = 0
    description = ""
    tile = None

    def move(self, dxdy):
        dx, dy = dxdy
        old_pos = self.tile.pos
        x, y = old_pos
        new_pos = (x+dx, y+dy)

        if self.tile.board.move_entity(self, old_pos, new_pos):
            self.on_move(old_pos, new_pos)
            return True

        return False

    def on_move(self, old_pos, new_pos):
        pass

    def on_despawn(self):
        pass

    def on_spawn(self):
        pass

    def on_first_seen(self):
        pass

    def is_in_fov(self):
        return self.tile.visible

    def default_interaction(self, actor):
        return None

    def draw(self):
        return (self.glyph, self.color, self.bgcolor)

    def update_glyph(self):
        pass


class Obstacle(Entity):
    blocks_movement = True
    blocks_vision = True
    is_wall = False
    is_door = False

    def default_interaction(self, actor):
        return interact.ExamineAction(actor, self)


class Decoration(Entity):
    pass
