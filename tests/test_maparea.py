
from rl.util import partition
from rl.board.generators import maparea

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
        a1 = maparea.MapArea(p1)
        a2 = maparea.MapArea(p2)
        
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
        a1 = maparea.MapArea(p1)
        a2 = maparea.MapArea(p2)
        
        areas = [a1, a2]
        
        for area in areas:
            area.find_neighbors(areas)
            
        assert a1 in [a['neighbor'] for a in a2.adjacent]
        assert a2 in [a['neighbor'] for a in a1.adjacent]
                
        assert a1.adjacent[0]['points'][0] == (0, 0)
        assert a2.adjacent[0]['points'][0] == (0, 1)
        
        assert len(a1.adjacent) == 1
        assert len(a2.adjacent) == 1
        
    def test_find_neighbors_irregular(self):
        """
            checks if these areas can find each other correctly
            +-+-+-+-+
            |1|2|3  |
            +-+ +-+-+
            |4| |5|6|
            +-+-+-+-+
        """
        
        p1 = partition.Partition((0, 0), 1, 1)
        p2 = partition.Partition((1, 0), 1, 2)
        p3 = partition.Partition((2, 0), 2, 1)
        p4 = partition.Partition((0, 1), 1, 1)
        p5 = partition.Partition((2, 1), 1, 1)
        p6 = partition.Partition((3, 1), 1, 1)
        
        a1 = maparea.MapArea(p1)
        a2 = maparea.MapArea(p2)
        a3 = maparea.MapArea(p3)
        a4 = maparea.MapArea(p4)
        a5 = maparea.MapArea(p5)
        a6 = maparea.MapArea(p6)
        
        areas = [a1, a2, a3, a4, a5, a6]
        
        for area in areas:
            area.find_neighbors(areas)
            
        assert len(a1.adjacent) == 2
        assert a4 in [a['neighbor'] for a in a1.adjacent]
        assert a2 in [a['neighbor'] for a in a1.adjacent]
        
        assert len(a2.adjacent) == 4
        assert a1 in [a['neighbor'] for a in a2.adjacent]
        assert a3 in [a['neighbor'] for a in a2.adjacent]
        assert a4 in [a['neighbor'] for a in a2.adjacent]
        assert a5 in [a['neighbor'] for a in a2.adjacent]
        
        # make sure the points are correct
        for a in a2.adjacent:
            if a['neighbor'] == a1 or a['neighbor'] == a3:
                assert a['points'] == [(1, 0)]
                
            elif a['neighbor'] == a4 or a['neighbor'] == a5:
                assert a['points'] == [(1, 1)]
                
        assert len(a3.adjacent) == 3
        assert a2 in [a['neighbor'] for a in a3.adjacent]
        assert a5 in [a['neighbor'] for a in a3.adjacent]
        assert a6 in [a['neighbor'] for a in a3.adjacent]
        
        # make sure the points are correct
        for a in a3.adjacent:
            if a['neighbor'] == a2:
                assert a['points'] == [(2, 0)]
                
            elif a['neighbor'] == a5:
                assert a['points'] == [(2, 0)]
                
            elif a['neighbor'] == a5:
                assert a['points'] == [(3, 0)]
        