import pytest

from util import partition

class TestPartition(object):
    
    def test_find_neighbors_horizontal(self):
        """
            checks if these partitions can find each other:
            +-+-+
            |1|2|
            +-+-+
        """
        
        p1 = partition.Partition((0,0), 1, 1)
        p2 = partition.Partition((1, 0), 1, 1)
        
        partitions = [p1, p2]
        
        for part in partitions:
            part.find_neighbors(partitions)
            
        assert p1 in [p[0] for p in p2.adjacent]
        assert p2 in [p[0] for p in p1.adjacent]
                
        assert p1.adjacent[0][1][0] == (0, 0)
        assert p2.adjacent[0][1][0] == (1, 0)
        
        assert len(p1.adjacent) == 1
        assert len(p2.adjacent) == 1
        
    def test_find_neighbors_vertical(self):
        """
            checks if these partitions can find each other:
            +-+
            |1|
            +-+
            |2|
            +-+
        """
        
        p1 = partition.Partition((0,0), 1, 1)
        p2 = partition.Partition((0,1), 1, 1)
        
        partitions = [p1, p2]
        
        for part in partitions:
            part.find_neighbors(partitions)
            
        assert p1 in [p[0] for p in p2.adjacent]
        assert p2 in [p[0] for p in p1.adjacent]
                
        assert p1.adjacent[0][1][0] == (0, 0)
        assert p2.adjacent[0][1][0] == (0, 1)
        
        assert len(p1.adjacent) == 1
        assert len(p2.adjacent) == 1