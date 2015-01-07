from rl.ui import colors
import textwrap

class Menu(object):
    def __init__(self, items, empty="There are no items."):
        self.items_raw = items
        self.items = {}
        
        self.empty = empty
        for k, v in items.items():
            self.items[k] = str(v)
        self.keys = sorted(items.keys())
        
        if self.keys:
            self.selected = self.keys[0]
        
    def move_to(self, key):
        if key in self.keys:
            self.selected = key
        
    def move_up(self):
        if not self.items:
            return
        i = self.keys.index(self.selected)
        new_pos = i-1
        
        if len(self.keys) < new_pos:
            new_pos = -1
        self.selected = self.keys[new_pos]
        
    def move_down(self):
        if not self.items:
            return
        i = self.keys.index(self.selected)
        new_pos = i+1
        if new_pos >= len(self.keys):
            new_pos = 0
        
        self.selected = self.keys[new_pos]
        
    def get_lines(self):
        lines = []
        
        if not self.items:
            return {
                "line": self.empty,
                "color": colors.white,
                "selected": False
            }
        
        for k in self.keys:
            item = self.items[k]
            ls = textwrap.wrap(item)
            ls[0] = k + ') ' + ls[0]
            for l in ls:
                lines.append({
                    'line': l,
                    'color': colors.white,
                    'selected': (self.selected == k)
                })
                
        return lines
        
    def get_selected(self, key=None):
        if not self.items:
            return None
        
        if key:
            if key not in self.keys:
                return None
                
            self.move_to(key)
            
        return self.items_raw[self.selected]
            