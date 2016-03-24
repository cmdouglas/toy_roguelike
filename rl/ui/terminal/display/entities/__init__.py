
class EntityDisplay:
    def __init__(self, entity):
        self.entity = entity
        self.entity.display = self

    def draw(self, tile):
        return (' ', None, None)


class BasicEntityDisplay(EntityDisplay):
    def __init__(self, entity, glyph, color, bgcolor=None):
        super().__init__(entity)
        self.glyph = glyph
        self.color = color
        self.bgcolor = bgcolor

    def draw(self, tile):
        return (self.glyph, self.color, self.bgcolor)
