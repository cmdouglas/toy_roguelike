
class Entity(object):
    article="a"
    name = ""
    name_plural = ""
    type = 'entity'

    blocks_movement = False
    blocks_vision = False

    interest_level = 0

    description = ""
    tile = None

    def persist_fields(self):
        return []

    @property
    def pos(self):
        if not self.tile:
            return None
        return self.tile.pos

    def on_move(self, old_pos, new_pos):
        pass

    def on_first_seen(self):
        pass

    def default_interaction(self, actor):
        return None

    def describe(self, num=1):
        if num != 1:
            article = str(num)
            name = self.name_plural
        else:
            article = self.article
            name = self.name

        r = "{article} {name}".format(article=article, name=name)

        return r

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        pass