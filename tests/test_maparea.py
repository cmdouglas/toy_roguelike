import pytest

from util import partition
from board.generators import pcpgenerator

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
        a1 = pcpgenerator.MapArea(p1)
        a2 = pcpgenerator.MapArea(p2)
        
        areas = [a1, a2]
        
        for area in areas:
            area.find_neighbors(areas)
            
        assert a1 in [a['neighbor'] for a in a2.adjacent]
        assert a2 in [a['neighbor'] for a in a1.adjacent]
                
        assert a1.adjacent[0]['points'][0] == (0, 0)
        assert a2.adjacent[0]['points'][0] == (1, 0)
        
        assert len(a1.adjacent) == 1
        assert len(a2.adjacent) == 1
        
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
        a1 = pcpgenerator.MapArea(p1)
        a2 = pcpgenerator.MapArea(p2)
        
        areas = [a1, a2]
        
        for area in areas:
            area.find_neighbors(areas)
            
        assert a1 in [a['neighbor'] for a in a2.adjacent]
        assert a2 in [a['neighbor'] for a in a1.adjacent]
                
        assert a1.adjacent[0]['points'][0] == (0, 0)
        assert a2.adjacent[0]['points'][0] == (0, 1)
        
        assert len(a1.adjacent) == 1
        assert len(a2.adjacent) == 1
