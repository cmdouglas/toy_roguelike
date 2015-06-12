from rl.ui import colors

class Entity(object):
    article="a"
    name = ""
    name_plural = ""

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

    def persist_fields(self):
        return []

    def move(self, dxdy):
        dx, dy = dxdy
        old_pos = self.tile.pos
        x, y = old_pos
        new_pos = (x+dx, y+dy)

        if self.tile.board.move_entity(self, old_pos, new_pos):
            self.on_move(old_pos, new_pos)
            return True

        return False

    @property
    def pos(self):
        if not self.tile:
            return None
        return self.tile.pos

    def on_move(self, old_pos, new_pos):
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

    def describe(self, num=1):
        if num != 1:
            article = str(num)
            name = self.name_plural
        else:
            article = self.article
            name = self.name

        r = "{article} {name}".format(article=article, name=name)

        return r