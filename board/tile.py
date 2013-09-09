import libtcodpy as libtcod

class Tile(object):
    def __init__(self, board, pos):
        self.pos = pos
        self.board = board
        self.objects = []
        
    def blocks_movement(self):
        for ob in self.objects:
            if ob.blocks_movement:
                return True
        
        return False
        
    def blocks_vision(self):
        for ob in self.objects:
            if ob.blocks_vision:
                return True
        
        return False
        
    def empty(self):
        self.objects = []
        
    def add_object(self, ob):
        if ob not in self.objects:
            self.objects.append(ob)
            ob.tile = self
            
    def remove_object(self, ob):
        if ob in self.objects:
            self.objects.remove(ob)
        
    def draw(self):
        x, y = self.pos
        color = libtcod.white
        char = '.'
        for ob in self.objects:
            color = ob.color
            char = ob.char
            
        return (char, color)
        
        
    def surrounding(self):
        """returns up to 8 surrounding tiles, fewer if called from an 
        edge or corner"""
        x, y = self.pos
        
        neighbors = [
            (x, y+1),   # north
            (x+1, y+1), # northeast
            (x+1, y),   # east
            (x+1, y-1), # southeast
            (x, y-1),   # south
            (x-1, y-1), # southwest
            (x-1, y),   # west
            (x-1, y+1), # northwest
        ]

        return [self.board[neighbor] for neighbor in neighbors 
            if self.board.position_is_valid(neighbor)]

                            
    def adjacent(self):
        """returns the 4 adjacent tiles, fewer if called from an edge or 
        corner"""
        x, y = self.pos
        
        neighbors = [
            (x, y+1),   # north
            (x+1, y),   # east
            (x, y-1),   # south
            (x-1, y),   # west
        ]

        return [self.board[neighbor] for neighbor in neighbors 
            if self.board.position_is_valid(neighbor)]
        
        
                            
    
                    