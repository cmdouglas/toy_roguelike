from collections import Counter

from rl.io import colors
from rl.util.tools import clamp

class HUD(object):

    def objects_of_interest(self, board):
        interesting_objects = []
        for pos in board.visible_to_player:
            if board.position_is_valid(pos):
                ob = board[pos].most_interesting_object()
                if ob:
                    interesting_objects.append(ob)
                
        interesting_objects.sort(key=lambda o: o.interest_level)
        
        interesting_objects_condensed = []
        c = Counter()
        
        for ob in interesting_objects:
            if ob.__class__ not in c:
                interesting_objects_condensed.append(ob)
            
            c.update([ob.__class__])
            
        r = []
        for ob in interesting_objects_condensed:
            count = c[ob.__class__]
            description = "A " + ob.describe()
            if count > 1:
                description = "%s %s" % (count, ob.name_plural)
                
            char = ob.char
            color = ob.color
            
            r.append({
                'description': description,
                'chars': min(count, 5)*char,
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
        
        
    
        
                