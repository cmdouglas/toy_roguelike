
class EntityDisplayManager:
    def __init__(self):
        self.entity_display_map

class EntityDisplay:
    def __init__(self, entity):
        self.entity = entity
        self.entity.display = self

    def draw(self):
        return (' ', None, None)


class BasicEntityDisplay(EntityDisplay):
    def __init__(self, entity, glyph, color, bgcolor=None):
        super().__init__(entity)
        self.glyph = glyph
        self.color = color
        self.bgcolor = bgcolor

    def draw(self):
        return (self.glyph, self.color, self.bgcolor)
