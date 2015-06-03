from collections import Counter

from rl.ui import colors
from rl.util.tools import clamp


class HUD(object):

    def objects_of_interest(self, world):
        board = world.board
        player = world.player
        interesting_objects = board.interesting_visible_entities(player)

        interesting_objects_condensed = []
        c = Counter()

        for ob in interesting_objects:
            if ob.__class__ not in c:
                interesting_objects_condensed.append(ob)

            c.update([ob.__class__])

        r = []
        for ob in interesting_objects_condensed:
            count = c[ob.__class__]
            description = ob.describe()

            glyph = ob.glyph
            color = ob.color

            r.append({
                'description': description.capitalize(),
                'glyphs': min(count, 5)*glyph,
                'color': color
            })

        return r

    def status_bar(self, value, max_value, statuscolors=None, bar_length=25):
        value = clamp(value, max_value)

        if not statuscolors:
            statuscolors = {
                'full': colors.light_green,
                'empty': colors.red
            }

        full = int(round((float(value)/max_value) * bar_length))
        empty = bar_length - full

        return {
            'full': full,
            'empty': empty,
            'colors': statuscolors
        }
