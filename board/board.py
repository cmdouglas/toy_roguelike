import logging

from gameobjects.smoothwall import SmoothWall
from gameobjects.actors.player import Player
from io import colors

class Tile(object):
    def __init__(self, board, pos):
        self.pos = pos
        self.board = board
        self.visible = False
        self.remembered = ' '
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
        for k, ob in self.objects.iteritems():
            if type(ob) == list:
                for o in ob:
                    if o and o.blocks_vision:
                        return True
            elif ob and ob.blocks_vision:
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

    def remembered_char(self):
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
            
        return char
        
    def draw(self):
        
        color = colors.light_gray
        bgcolor = colors.black

        if self.visible:
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
        else:
            char = self.remembered
            color = colors.dark_gray
            bgcolor = colors.black
            
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
        self.player = None
        self.visible_to_player = set()
        
        self.tiles = [[Tile(self, (x, y)) for y in xrange(self.height)] 
            for x in range(self.width)]
            
        self.areas = []
        self.setup()
        
    def setup(self):
        pass
    
    def show_player_fov(self):
        for row in self.tiles:
            for tile in row:
                tile.visible = False
        
        visible_points = self.get_visible_points(self.player.tile.pos, self.player.sight_radius)
        
        for point in visible_points:
            if self.position_is_valid(point):
                tile = self[point]
                tile.remembered = tile.remembered_char()
                tile.visible = True
            
    
    def __getitem__(self, pos):
        x, y = pos
        return self.tiles[x][y]
    
    def position_is_valid(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height
        
    def area_containing_point(self, pos):
        for area in self.areas:
            if area.contains_point(pos):
                return area
                
        return None

    def nearby_reachable_points(self, pos, distance):
        points = []
        
        def _add_empty_neighbors(p,d):
            candidates = self[p].surrounding()
            for candidate in candidates:
                if (not candidate.blocks_movement() and
                    not candidate.pos in points):
                
                    points.append(candidate.pos)
                    if d > 0:
                        _add_empty_neighbors(candidate.pos, d-1)
        _add_empty_neighbors(pos, distance)
        
        return points
                
        
    def get_visible_points(self, pos, radius):
        directions = [
            (1,  0,  0,  1),
            (0,  1,  1,  0),
            (0, -1,  1,  0),
            (-1, 0,  0,  1),
            (-1, 0,  0, -1),
            (0, -1, -1,  0),
            (0,  1, -1,  0),
            (1,  0,  0, -1)
        ]
        
        visible = []
        
        def is_blocked(pos):
            return not self.position_is_valid(pos) or self[pos].blocks_vision()
        
        def cast_light(center, row, start, end, radius, mult, id=0):
            "Recursive lightcasting function"
            cx, cy = center
            xx, xy, yx, yy = mult

            if start < end:
                return
            radius_squared = radius*radius
            for j in range(row, radius+1):
                dx, dy = -j-1, -j
                blocked = False
                while dx <= 0:
                    dx += 1
                    # Translate the dx, dy coordinates into map coordinates:
                    x, y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                    # l_slope and r_slope store the slopes of the left and right
                    # extremities of the square we're considering:
                    l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
                    if start < r_slope:
                        continue
                    elif end > l_slope:
                        break
                    else:
                        # Our light beam is touching this square; light it:
                        if dx*dx + dy*dy < radius_squared:
                            visible.append((x, y))
                        if blocked:
                            # we're scanning a row of blocked squares:
                            if is_blocked((x, y)):
                                new_start = r_slope
                                continue
                            else:
                                blocked = False
                                start = new_start
                        else:
                            if is_blocked((x, y)) and j < radius:
                                # This is a blocking square, start a child scan:
                                blocked = True
                                cast_light(center, j+1, start, l_slope,
                                                 radius, mult, id+1)
                                new_start = r_slope
                # Row is scanned; do next row unless last square was blocked:
                if blocked:
                    break
                    
        for d in directions:
            cast_light(pos, 1, 1.0, 0.0, radius, d)
            
        return visible
        
    def add_object(self, ob, pos):
        tile = self[pos]
        try:
            tile.add_object(ob)
            self.objects.append(ob)
            ob.tile = tile
            if type(ob) == Player:
                self.player = ob
                
            ob.on_spawn()
            
        
        except(GameObjectPlacementException):
            logging.error("Couldn't place object %s at position %s", ob, pos)
            raise
        
    def remove_object(self, ob):
        if not ob:
            #logging.warn("Trying to remove an object that doesn't exist!")
            return
            
        ob.tile.remove_object(ob)
        self.objects.remove(ob)
        ob.on_despawn()
        ob.tile = None
        
    def move_object(self, ob, old_pos, new_pos):
        if self.position_is_valid(new_pos):
            old_tile = self[old_pos]
            new_tile = self[new_pos]
            x1, y1 = old_pos
            x2, y2 = new_pos
            
            if not new_tile.blocks_movement():
                old_tile.remove_object(ob)
                new_tile.add_object(ob)
                ob.tile = new_tile
                ob.on_move(x2-x1, y2-y1)
                
                return True
                
        return False
        
class GameObjectPlacementException(Exception):
    pass