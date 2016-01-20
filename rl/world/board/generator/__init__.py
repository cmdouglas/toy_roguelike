import random

from rl.util import dice
from rl.util import partition
from rl.world.board import Board
from rl.world.board.region import MapRegion
from rl.world.board.generator.painters import shapedroom
from rl.world.board.generator.painters import tunnel
from rl.world.board.generator.painters import cave
from rl.world.board.generator.painters import maze
from rl.world.board.generator.painters import roomcluster
from rl.world.entities.actors.goblin import Goblin
from rl.world.entities.actors.ogre import Ogre
from rl.world.entities.items.potion import HealingPotion
from rl.world.entities.items.scroll import TeleportationScroll


class PartitionStrategy(object):
    pass


class RegularGridPartitionStrategy(PartitionStrategy):
    def __init__(self):
        pass

    def partition(self, board, partition_width, partition_height):
        part = partition.Partition((0, 0), board.width, board.height)

        rectangles = [p.to_rectangle for p in
                      part.subpartition_regular_grid(partition_width, partition_height)]

        regions = [MapRegion(rect, board) for rect in rectangles]
        for region in regions:
            region.find_neighbors(regions)

        return regions


class BSPPartitionStrategy(object):
    def partition(self, board, min_width, min_height):
        part = partition.Partition((0, 0), board.width, board.height)

        rectangles = [p.to_rectangle() for p in part.subpartition_bsp(min_width, min_height)]

        regions = [MapRegion(rect, board) for rect in rectangles]
        for region in regions:
            region.find_neighbors(regions)

        return regions


class ConnectionStrategy(object):
    pass


class PainterStrategy(object):
    pass


class RandomPainterStrategy(PainterStrategy):
    def __init__(self):
        self.painters = [
            shapedroom.RectangularRoomPainter,
            shapedroom.CircularRoomPainter,
            shapedroom.EllipticalRoomPainter,
            tunnel.SnakeyTunnelPainter,
            # greathall.GreatHallPainter,
            roomcluster.RoomClusterPainter,
            maze.MazePainter,
            cave.CavePainter
        ]

    def paint(self, board):
        for region in board.regions:
            painters = [p for p in self.painters if p.region_meets_requirements(region)]

            painter = random.choice(painters)(board, region)

            painter.paint()


class SimpleWebConnectionStrategy(ConnectionStrategy):
    def connect(self, regions):
        unconnected = regions[:]
        frontier = []

        # pick a random region
        start = random.choice(unconnected)
        unconnected.remove(start)

        # connect to each neighbor
        for region in start.connectible_neighbors():
            start.connect_to(region)
            unconnected.remove(region)
            frontier.append(region)

        while len(unconnected) > 0:
            # print unconnected

            changed = False
            for region in frontier[:]:
                frontier.remove(region)
                neighbors = region.connectible_neighbors()
                unconnected_neighbors = [n for n in neighbors
                                         if n in unconnected]

                # maybe connect to a random neighbor just for kicks
                if dice.one_chance_in(3):
                    region.connect_to(random.choice(neighbors))

                # but always connect to an unconnected neighbor, if one exists.
                if unconnected_neighbors:
                    changed = True
                    n = random.choice(unconnected_neighbors)
                    region.connect_to(n)
                    unconnected.remove(n)
                    frontier.append(n)

            if not changed and unconnected:
                start = random.choice(unconnected)
                unconnected.remove(start)
                for region in start.connectible_neighbors():
                    start.connect_to(region)
                    if region in unconnected:
                        unconnected.remove(region)
                        frontier.append(region)


class Generator(object):
    def __init__(self):
        self.partition_strategy = BSPPartitionStrategy()
        self.connection_strategy = SimpleWebConnectionStrategy()
        self.painter_strategy = RandomPainterStrategy()

    def generate(self, width=80, height=80, world=None):
        b = Board(width, height, world)
        b.regions = self.partition_strategy.partition(b, 12, 12)
        self.connection_strategy.connect(b.regions)
        self.painter_strategy.paint(b)

        for i in range(20):
            region = random.choice(b.regions)
            point = random.choice(region.empty_points())

            b.add_entity(Goblin(), point)

        for i in range(5):
            region = random.choice(b.regions)
            point = random.choice(region.empty_points())

            b.add_entity(HealingPotion(), point)

        for i in range(5):
            region = random.choice(b.regions)
            point = random.choice(region.empty_points())

            b.add_entity(TeleportationScroll(), point)

        region = random.choice(b.regions)
        point = random.choice(region.empty_points())
        b.add_entity(Ogre(), point)

        return b
