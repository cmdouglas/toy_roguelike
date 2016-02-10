from rl.ui.terminal.display import colors, glyphs
from rl.ui.terminal.display.entities import BasicEntityDisplay
from rl.ui.terminal.display.entities.creature import CreatureDisplay
from rl.ui.terminal.display.entities.wall import WallDisplay

class EntityRenderer:
    def __init__(self):
        self.render_map = {
            'player': (CreatureDisplay, ('@', colors.bright_white, None)),

            'goblin': (CreatureDisplay, ('g', colors.green, None)),
            'ogre': (CreatureDisplay, ('O', colors.bright_red, None)),

            'healing_potion': (BasicEntityDisplay, ('!', colors.bright_yellow, None)),
            'teleportation_scroll': (BasicEntityDisplay, ('!', colors.bright_white, None)),

            'wall': (WallDisplay, ),
            'floor': (BasicEntityDisplay, ('.', colors.white, None)),
        }
