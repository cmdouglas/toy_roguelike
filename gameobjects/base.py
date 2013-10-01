from io import colors

class GameObject(object):
    color = colors.light_gray
    bgcolor = colors.black
    char = ' '
    blocks_movement = False
    blocks_vision = False
    can_act = False
    can_be_taken = False
            
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
    can_be_taken = True
    
class Decoration(GameObject):
    pass