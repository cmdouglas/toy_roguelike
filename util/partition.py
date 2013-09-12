"""

"""
TOP, BOTTOM, LEFT, RIGHT = 0, 1, 2, 3

class Partition(object):

    def __init__(self, ul_pos, width, height):
        self.ul_pos = ul_pos
        self.width = width
        self.height = height
        self.adjacent = []
        self.connected = []
        
    def __repr__(self):
        return "Partition(%s, %s, %s)" % (self.ul_pos, self.width, self.height)
        
    def contains_point(self, p):
        x, y = p
        self_x, self_y = self.ulpos
        return (self_x <= x < self_x + self.width and
                self_y <= y < self_y + self.height)
        
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
                
                self.adjacent.append((other, self.find_adjacent_points(other, TOP)))
               
            # adjacent on bottom 
            elif (self_bottom + 1 == other_top and
                other_left <= self_right and
                self_left <= other_right):
                
                self.adjacent.append((other, self.find_adjacent_points(other, BOTTOM)))
            
            # adjacent on left
            elif (self_left - 1 == other_right and
                other_top <= self_bottom and
                self_top <= other_bottom):
                
                self.adjacent.append((other, self.find_adjacent_points(other, LEFT)))
            
            # adjacent on right
            elif (self_right + 1 == other_left and
                other_top <= self_bottom and
                self_top <= other_bottom):
                
                self.adjacent.append((other, self.find_adjacent_points(other, RIGHT)))
                    
        return self.adjacent
    
    def subpartition_simple_grid(self, partition_width, partition_height):
        assert self.width % partition_width == 0
        assert self.height % partition_height == 0
        
        partitions = []
        
        for y in range(self.height / partition_height):
            for x in range(self.width / partition_width):
                ulcorner = (x * partition_width, y * partition_height)
                partitions.append(Partition(ulcorner, partition_width, partition_height))
                
        for p in partitions:
            p.find_neighbors(partitions)
            
        return partitions
        
    def subpartition_bsp(self, max_size, min_size):
        pass
    
    
        