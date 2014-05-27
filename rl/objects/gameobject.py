import math
from rl.io import colors

class GameObject(object):
    color = colors.light_gray
    bgcolor = colors.black
    char = ' '
    blocks_movement = False
    blocks_vision = False
    can_act = False
    can_be_taken = False
    interest_level = 0
            
    def move(self, dxdy):
        dx, dy = dxdy
        old_pos = self.tile.pos
        x, y = old_pos
        new_pos = (x+dx, y+dy)
        
        if self.tile.board.move_object(self, old_pos, new_pos):
            self.on_move(old_pos, new_pos)
            return True
            
        return False
                
    def on_despawn(self):
        pass
        
    def on_spawn(self):
        pass
        
    def is_in_fov(self):
        return self.tile.visible
        
class Actor(GameObject):
    blocks_movement = True
    can_act = True
    
    def on_move(self, old_pos, new_pos):
        pass
        
    def process_turn(self):
        return False
    
class Obstacle(GameObject):
    blocks_movement = True
    blocks_vision = True
    
class Item(GameObject):
    usable = False
    equippable = False
    stack_size = 1
    name = ""
    name_plural = ""
    
    def describe(self):
        if self.stack_size == 1:
            return "a %s" % self.name
        else:
            return "%d %s" % (self.stack_size, self.name_plural)
    
    def __str__(self):
        return self.describe()
    
class Decoration(GameObject):
    pass