
from rl.util import partition
from rl.board.region import MapRegion
from rl.board.board import Board

class TestRegion(object):

    def test_find_neighbors_horizontal(self):
        b = Board(2, 1)
        """
            checks if these partitions can find each other:
            +-+-+
            |1|2|
            +-+-+
        """

        p1 = partition.Partition((0,0), 1, 1).to_rectangle()
        p2 = partition.Partition((1, 0), 1, 1).to_rectangle()
        r1 = MapRegion(p1, b)
        r2 = MapRegion(p2, b)

        regions = [r1, r2]


        for region in regions:
            region.find_neighbors(regions)

        assert r1 in r2.adjacent.keys()
        assert r2 in r1.adjacent.keys()

        assert (0, 0) in r1.adjacent[r2]
        assert (1, 0) in r2.adjacent[r1]

        assert len(r1.adjacent) == 1
        assert len(r2.adjacent) == 1

    def test_find_neighbors_vertical(self):
        """
            checks if these partitions can find each other:
            +-+
            |1|
            +-+
            |2|
            +-+
        """
        b = Board(1, 2)
        p1 = partition.Partition((0, 0), 1, 1).to_rectangle()
        p2 = partition.Partition((0, 1), 1, 1).to_rectangle()
        r1 = MapRegion(p1, b)
        r2 = MapRegion(p2, b)

        regions = [r1, r2]

        for region in regions:
            region.find_neighbors(regions)

        assert r1 in r2.adjacent.keys()
        assert r2 in r1.adjacent.keys()

        assert (0, 0) in r1.adjacent[r2]
        assert (0, 1) in r2.adjacent[r1]

        assert len(r1.adjacent) == 1
        assert len(r2.adjacent) == 1

    def test_find_neighbors_irregular(self):
        """
            checks if these areas can find each other correctly
            +-+-+-+-+
            |1|2|3  |
            +-+ +-+-+
            |4| |5|6|
            +-+-+-+-+
        """
        b = Board(4, 2)
        p1 = partition.Partition((0, 0), 1, 1).to_rectangle()
        p2 = partition.Partition((1, 0), 1, 2).to_rectangle()
        p3 = partition.Partition((2, 0), 2, 1).to_rectangle()
        p4 = partition.Partition((0, 1), 1, 1).to_rectangle()
        p5 = partition.Partition((2, 1), 1, 1).to_rectangle()
        p6 = partition.Partition((3, 1), 1, 1).to_rectangle()

        r1 = MapRegion(p1, b)
        r2 = MapRegion(p2, b)
        r3 = MapRegion(p3, b)
        r4 = MapRegion(p4, b)
        r5 = MapRegion(p5, b)
        r6 = MapRegion(p6, b)

        regions = [r1, r2, r3, r4, r5, r6]

        for region in regions:
            region.find_neighbors(regions)

        assert len(r1.adjacent) == 2

        assert r4 in r1.adjacent.keys()
        assert (0, 0) in r1.adjacent[r4]

        assert r2 in r1.adjacent.keys()
        assert (0, 0) in r1.adjacent[r2]

        assert len(r2.adjacent) == 4

        assert r1 in r2.adjacent.keys()
        assert (1, 0) in r2.adjacent[r1]

        assert r3 in r2.adjacent.keys()
        assert (1, 0) in r2.adjacent[r3]

        assert r4 in r2.adjacent.keys()
        assert (1, 1) in r2.adjacent[r4]

        assert r5 in r2.adjacent.keys()
        assert (1, 1) in r2.adjacent[r5]

