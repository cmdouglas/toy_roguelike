"""

"""
import random
import collections


class PartitionException(Exception):
    pass

class Partition(object):

    def __init__(self, ul_pos, width, height):
        self.ul_pos = ul_pos
        self.width = width
        self.height = height
        
    def __repr__(self):
        return "Partition(%s, %s, %s)" % (self.ul_pos, self.width, self.height)
        
    def contains_point(self, p):
        x, y = p
        self_x, self_y = self.ulpos
        return (self_x <= x < self_x + self.width and
                self_y <= y < self_y + self.height)
        
    
    def subpartition_simple_grid(self, partition_width, partition_height):
        assert self.width % partition_width == 0
        assert self.height % partition_height == 0
        
        partitions = []
        
        for y in range(self.height / partition_height):
            for x in range(self.width / partition_width):
                ulcorner = (x * partition_width, y * partition_height)
                partitions.append(Partition(ulcorner, partition_width, partition_height))
            
        return partitions
        
    def subpartition_bsp(self, min_width, min_height):
        """recursively divide in 2 until all pieces are between min_size and 
        2*min_size.
        """
        
        def split_horizontal(p):
            ul_x, ul_y = p.ul_pos
            print "choosing a horizontal point between %s and %s" % (ul_x + min_width, ul_x + p.width - min_width + 1)
            
            split_pos = (random.choice(
                range(ul_x + min_width, ul_x + p.width - min_width + 1)), ul_y)
                
            split_x, split_y = split_pos
                
            return([Partition(p.ul_pos, split_x-ul_x, p.height), 
                    Partition(split_pos, ul_x + p.width - split_x, p.height)])
                    
        def split_vertical(p):
            ul_x, ul_y = p.ul_pos
            print "choosing a vertical point between %s and %s" % (ul_y + min_height, ul_y + p.height - min_height + 1)
            
            split_pos = (ul_x, random.choice(
                range(ul_y + min_height, ul_y + p.height - min_height + 1)))
                
            split_x, split_y = split_pos
                
            return([Partition(p.ul_pos, p.width, split_y-ul_y), 
                    Partition(split_pos, p.width, ul_y + p.height - split_y)])
                    
        def flatten(l):
            for el in l:
                if (isinstance(el, collections.Iterable) and 
                    not isinstance(el, basestring)):
                    for sub in flatten(el):
                        yield sub
                else:
                    yield el
        
        if self.width < min_width or self.height < min_height:
            print self
            raise PartitionException("Partition too small!")
        
        splith = (self.width > 2*min_width)
        splitv = (self.height > 2*min_height)
        
        new_partitions = None
        
        if splith and splitv:
            new_partitions = random.choice([
                split_horizontal, split_vertical])(self)
            
        elif splith:
            new_partitions = split_horizontal(self)
            
        elif splitv:
            new_partitions = split_vertical(self)
            
        else:
            return self
            
        return list(flatten([p.subpartition_bsp(min_width, min_height) 
            for p in new_partitions]))

            