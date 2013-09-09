import libtcodpy as libtcod
import logging

class Tile(object):
    def __init__(self, board, pos):
        self.pos = pos
        self.board = board
        self.objects = {
            'obstacle': None,
            'actor': None,
            'items': [],
            'decorations': []
        }
        
    def blocks_movement(self):
        if (self.objects['obstacle'] and 
            self.objects['obstacle'].blocks_movement):
            return True
            
        if (self.objects['actor'] and 
            self.objects['actor'].blocks_movement):
            return True
        
        return False
        
    def blocks_vision(self):
        for ob in self.objects:
            if ob.blocks_vision:
                return True
        
        return False
        
    def add_actor(self, ob):
        if self.objects['actor'] is not None:
            raise GameObjectPlacementException("Tried to add an actor to a"
             "square that already has one")
        self.objects['actor'] = ob
        
    def add_obstacle(self, ob):
        if self.objects['obstacle'] is not None:
            raise GameObjectPlacementException("Tried to add an obstacle" 
            "to a square that already has one")
        self.objects['obstacle'] = ob
        
    def add_item(self, ob):
        if ob not in self.objects['items']:
            self.objects.append(ob)

    def add_decoration(self, ob):
        if ob not in self.objects['decorations']:
            self.objects.append(ob)                
    
    def add_object(self, ob):
        if ob.can_act:
            self.add_actor(ob)
        elif ob.blocks_movement:
            self.add_obstacle(ob)
        elif ob.can_be_taken:
            self.add_item(ob)
        else:
            self.add_decoration(ob)
                        
    def remove_object(self, ob):
        if ob.can_act and self.objects['actor'] == ob:
            self.objects['actor'] = None
        elif ob.blocks_movement and self.objects['obstacle'] == ob:
            self.objects['obstacle'] = None
        elif ob.can_be_taken and ob in self.objects['items']:
            self.objects['items'].remove(ob)
        elif ob in self.objects['decorations']:
            self.objects['decorations'].remove(ob)

    def draw(self):
        color = libtcod.white
        bgcolor = libtcod.black
        char = '.'
        
        ob = None
        if self.objects['actor']:
            ob = self.objects['actor']
            
        elif self.objects['obstacle']:
            ob = self.objects['obstacle']
            
        elif self.objects['items']:
            ob = self.objects['items'][0]
            
        elif self.objects['decorations']:
            ob = self.objects['decorations'][0]
        
        if ob:
            char = ob.char
            color = ob.color
            bgcolor = ob.bgcolor
            
        return (char, color, bgcolor)
        
        
    def surrounding(self, as_dict=False):
        """returns up to 8 surrounding tiles, fewer if called from an 
        edge or corner"""
        x, y = self.pos
        
        neighbors = [
            (x, y-1),   # north
            (x+1, y-1), # northeast
            (x+1, y),   # east
            (x+1, y+1), # southeast
            (x, y+1),   # south
            (x-1, y+1), # southwest
            (x-1, y),   # west
            (x-1, y-1), # northwest
        ]
        
        if as_dict:
            r = {}
            dirs = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
            for i, neighbor in enumerate(neighbors):
                d = dirs[i]
                if self.board.position_is_valid(neighbor):
                    r[d] = self.board[neighbor]
                    
            return r
                
        return [self.board[neighbor] for neighbor in neighbors 
            if self.board.position_is_valid(neighbor)]

                            
    def adjacent(self, as_dict=False):
        """returns the 4 adjacent tiles, fewer if called from an edge or 
        corner"""
        x, y = self.pos
        
        neighbors = [
            (x, y-1),   # north
            (x+1, y),   # east
            (x, y+1),   # south
            (x-1, y),   # west
        ]

        if as_dict:
            r = {}
            dirs = ['n', 'e', 's', 'w']
            for i, neighbor in enumerate(neighbors):
                d = dirs[i]
                if self.board.position_is_valid(neighbor):
                    r[d] = self.board[neighbor]
                    
            return r

        return [self.board[neighbor] for neighbor in neighbors 
            if self.board.position_is_valid(neighbor)]


class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []
        
        self.tiles = [[Tile(self, (x, y)) for y in xrange(self.height)] 
            for x in range(self.width)]
            
        self.setup()
        
    def setup(self):
        pass
    
    def __getitem__(self, pos):
        x, y = pos
        return self.tiles[x][y]
    
    def position_is_valid(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height
        
    def add_object(self, ob, pos):
        tile = self[pos]
        try:
            tile.add_object(ob)
            self.objects.append(ob)
            ob.tile = tile
            ob.on_spawn()
        
        except(GameObjectPlacementException):
            logging.error("Couldn't place object %s at position %s", ob, pos)
            raise
        
    def remove_object(self, ob):
        if not ob:
            logging.warn("Trying to remove an object that doesn't exist!")
            return
            
        ob.tile.remove_object(ob)
        self.objects.remove(ob)
        ob.on_despawn()
        ob.tile = None
        
    def move_object(self, ob, old_pos, new_pos):
        if self.position_is_valid(new_pos):
            old_tile = self[old_pos]
            new_tile = self[new_pos]
            
            if not new_tile.blocks_movement():
                old_tile.remove_object(ob)
                new_tile.add_object(ob)
                ob.tile = new_tile
                
                return True
                
        return False
        
class GameObjectPlacementException(Exception):
    pass