"""
PCP generator (Partition, Connect, Paint)

1.  Partitions the board into areas according to some strategy
2.  Connects the areas to one another according to some strategy
3.  Paints each individual area according to some strategy

"""

from util import partition


TOP, BOTTOM, LEFT, RIGHT = 0, 1, 2, 3

class MapArea(object):
    def __init__(self, partition):
        self.ul_pos = partition.ul_pos
        self.width = partition.width
        self.height = partition.height
        self.adjacent = []
        self.connected = []
        
        self.connection_cost = 0
        self.keywords = []
        
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
            top = min(self_top, other_top)
            bottom = max(self_bottom, other_bottom)
            
            points = [(self_left, i) for i in range(top, bottom+1)]
            
        elif side == RIGHT:
            top = min(self_top, other_top)
            bottom = max(self_bottom, other_bottom)
            
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
                
                self.adjacent.append({
                    'neighbor': other, 
                    'points': self.find_adjacent_points(other, TOP)
                })
               
            # adjacent on bottom 
            elif (self_bottom + 1 == other_top and
                other_left <= self_right and
                self_left <= other_right):
                
                self.adjacent.append({
                    'neighbor': other, 
                    'points': self.find_adjacent_points(other, BOTTOM)
                })
            
            # adjacent on left
            elif (self_left - 1 == other_right and
                other_top <= self_bottom and
                self_top <= other_bottom):
                
                self.adjacent.append({
                    'neighbor': other, 
                    'points': self.find_adjacent_points(other, LEFT)
                })
            
            # adjacent on right
            elif (self_right + 1 == other_left and
                other_top <= self_bottom and
                self_top <= other_bottom):
                
                self.adjacent.append({
                    'neighbor': other, 
                    'points': self.find_adjacent_points(other, RIGHT)
                })
                    
        return self.adjacent

                
    
class PCPGenerator(object):
    def __init__(self):
        self.partition_strategy = None
        self.connection_strategy = None
        
    
    