import random

TOP, BOTTOM, LEFT, RIGHT = 0, 1, 2, 3

class MapAreaConnectionException(Exception):
    pass

class MapArea(object):
    def __init__(self, partition, board):
        self.board = board
        self.ul_pos = partition.ul_pos
        self.width = partition.width
        self.height = partition.height
        self.adjacent = []
        self.connections = []
        self.entrance = False
        self.points = set()

        self.connection_cost = 0
        self.keywords = []
        
    def __repr__(self):
        return "MapArea(%s, %s, %s)" % (self.ul_pos, self.width, self.height)

    def contains_point(self, p):
        x, y = p
        self_x, self_y = self.ul_pos
        return (self_x <= x < self_x + self.width and
                self_y <= y < self_y + self.height)

    def get_all_points(self):
        if not self.points:
            x0, y0 = self.ul_pos

            for x in [x for x in range(x0, x0+self.width)]:
                for y in [y for y in range(y0, y0+self.height)]:
                    self.points.add((x, y))

        return self.points

    def border(self):
        left, top = self.ul_pos
        right = left + self.width -1
        bottom = top + self.height - 1
        return [point for point in self.get_all_points()
                    if (point[0] == left
                        or point[0] == right
                        or point[1] == top
                        or point[1] == bottom)]
                
    def get_empty_points(self):
        return [point for point in self.get_all_points() if (
            not self.board[point].objects['obstacle'] and not self.board[point].objects['actor'])]
        
    def find_neighbor(self, other):
        for a in self.adjacent:
            if a['neighbor'] == other:
                return a
        return None
        
    def find_neighboring_point(self, neighbor, point):
        #print "finding a neighboring point to %s in %s" % (point, neighbor)
        for p in neighbor["points"]:
            x1, y1 = point
            x2, y2 = p
            
            c = (x2-x1, y2-y1)
            if c in [(0,1), (1, 0), (0,-1), (-1, 0)]:
                #print "found %s" % (p,)
                return p
                    
    def connect_to(self, other, point=None):
        adjacency = self.find_neighbor(other)
                
        if not adjacency:
            raise MapAreaConnectionException(
                "Trying to connect %s to a non-adjacent area %s" % (self, other))
                
        if not point:
            #pick connection point, avoiding the corners if possible
            if len(adjacency['points']) >= 3:
                point = random.choice(adjacency['points'][1:-1])
            else:
                raise Exception(str(adjacency))
                point = random.choice(adjacency['points'])
            other_adjacency = other.find_neighbor(self)
            neighbor_point = self.find_neighboring_point(other_adjacency, point)
            
        self.connections.append({
            'area': other,
            'point': point,
            'side': adjacency['side']
        })
        
        other.connections.append({
            'area': self,
            'point': neighbor_point,
            'side': self.corresponding_side(adjacency['side'])
        })

    def corresponding_side(self, side):
        return {
            LEFT: RIGHT,
            TOP: BOTTOM,
            RIGHT: LEFT,
            BOTTOM: TOP
        }.get(side)
        
    def find_adjacent_points(self, other, side):
        
        self_left, self_top = self.ul_pos
        self_bottom = self_top + self.height - 1
        self_right = self_left + self.width - 1
        
        other_left, other_top = other.ul_pos
        other_right = other_left + other.width - 1
        other_bottom = other_top + other.height - 1
        
        points = []
        
        if side == TOP:
            left = max(self_left, other_left)
            right = min(self_right, other_right)
            
            points = [(i, self_top) for i in range(left, right+1)]
                        
        elif side == BOTTOM:            
            left = max(self_left, other_left)
            right = min(self_right, other_right)
            
            points = [(i, self_bottom) for i in range(left, right+1)]            
            
        elif side == LEFT:
            top = max(self_top, other_top)
            bottom = min(self_bottom, other_bottom)
            
            points = [(self_left, i) for i in range(top, bottom+1)]
            
        elif side == RIGHT:            
            top = max(self_top, other_top)
            bottom = min(self_bottom, other_bottom)
            
            points = [(self_right, i) for i in range(top, bottom+1)]
            
        return points
        
    def find_neighbors(self, others):
        self_left, self_top = self.ul_pos
        self_bottom = self_top + self.height - 1
        self_right = self_left + self.width - 1
        
        for other in others:
            if other is self:
                continue

            if other in self.adjacent:
                continue

            other_left, other_top = other.ul_pos
            other_right = other_left + other.width - 1
            other_bottom = other_top + other.height - 1
                
            # adjacent on top
            if (self_top - 1 == other_bottom and
                other_left <= self_right and
                self_left <= other_right):
                adjacent = self.find_adjacent_points(other, TOP)

                if len(adjacent) >= 3:
                    self.adjacent.append({
                        'neighbor': other,
                        'points': adjacent,
                        'side': TOP
                    })
               
            # adjacent on bottom 
            elif (self_bottom + 1 == other_top and
                other_left <= self_right and
                self_left <= other_right):

                adjacent = self.find_adjacent_points(other, BOTTOM)
                if len(adjacent) >= 3:
                    self.adjacent.append({
                        'neighbor': other,
                        'points': adjacent,
                        'side': BOTTOM
                    })
            
            # adjacent on left
            elif (self_left - 1 == other_right and
                other_top <= self_bottom and
                self_top <= other_bottom):
                adjacent = self.find_adjacent_points(other, LEFT)
                if len(adjacent) >= 3:
                    self.adjacent.append({
                        'neighbor': other,
                        'points': adjacent,
                        'side': LEFT
                    })
            
            # adjacent on right
            elif (self_right + 1 == other_left and
                other_top <= self_bottom and
                self_top <= other_bottom):

                adjacent = self.find_adjacent_points(other, RIGHT)
                if len(adjacent) >= 3:
                    self.adjacent.append({
                        'neighbor': other,
                        'points': adjacent,
                        'side': RIGHT
                    })
                    
        return self.adjacent