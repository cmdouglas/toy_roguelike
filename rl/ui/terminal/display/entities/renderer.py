from rl.ui.terminal.display import colors, glyphs
from rl.ui.terminal.display.entities import BasicEntityDisplay
from rl.ui.terminal.display.entities.creature import CreatureDisplay
from rl.ui.terminal.display.entities.wall import WallDisplay

class EntityRenderer:
    def __init__(self):
        self.display_types = {
            'player': (CreatureDisplay, ('@', colors.bright_white, None)),

            'goblin': (CreatureDisplay, ('g', colors.green, None)),
            'ogre': (CreatureDisplay, ('O', colors.bright_red, None)),

            'healing_potion': (BasicEntityDisplay, ('!', colors.bright_yellow, None)),
            'teleportation_scroll': (BasicEntityDisplay, ('?', colors.bright_white, None)),

            'wall': (WallDisplay, ()),
            'floor': (BasicEntityDisplay, ('.', colors.white, None)),
            'open_door': (BasicEntityDisplay, (glyphs.open_box, colors.sepia, None)),
            'closed_door': (BasicEntityDisplay, ('+', colors.sepia, None))
        }

        self.entity_displays = {}

    def render(self, entity, tile):
        if entity not in self.entity_displays.keys():
            display_type, args = self.display_types.get(entity.type, (BasicEntityDisplay, ('?', colors.light_gray, None)))
            self.entity_displays[entity] = display_type(entity, *args)

        return self.entity_displays[entity].draw(tile)
