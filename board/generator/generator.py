
import random

from util import dice
from util import partition
from board import board
from board.generator import maparea
from board.generator.painters import shapedroom
from board.generator.painters import tunnel
from board.generator.painters import cave

    
class PartitionStrategy(object):
    pass


class RegularGridPartitionStrategy(PartitionStrategy):
    def __init__(self):
        pass
    
    def partition(self, board, partition_width, partition_height):
        part = partition.Partition((0, 0), board.width, board.height)
        
        ps = part.subpartition_regular_grid(partition_width, partition_height)
        
        areas = [maparea.MapArea(p) for p in ps]
        for area in areas:
            area.find_neighbors(areas)
        
        return areas

class BSPPartitionStrategy(object):
    def partition(self, board, min_width, min_height):
        part = partition.Partition((0, 0), board.width, board.height)
        
        ps = part.subpartition_bsp(min_width, min_height)
        
        areas = [maparea.MapArea(p) for p in ps]
        for area in areas:
            area.find_neighbors(areas)
        
        return areas

     
class ConnectionStrategy(object):
    pass


class PainterStrategy(object):
    pass
    
class RandomPainterStrategy(PainterStrategy):
    def __init__(self):
        self.painters = [
            shapedroom.RectangularRoomPainter(),
            shapedroom.CircularRoomPainter(),
            shapedroom.EllipticalRoomPainter(),
            #tunnel.SimpleTunnelPainter(),
            tunnel.SnakeyTunnelPainter(),
            cave.CavePainter()
        ]
        
    def paint(self, board):
        areas = board.areas
        player_start = random.choice(areas)
        areas = board.areas
        for area in areas:
            painter = random.choice([
                p for p in self.painters  if p.area_meets_requirements(area)
            ])
            
            painter.paint(board, area)
            
        painter.place_player(board, player_start)

    
class SimpleWebConnectionStrategy(ConnectionStrategy):
    def connect(self, areas):
        unconnected = areas[:]
        frontier = []
        
        # pick a random area
        start = random.choice(unconnected)
        unconnected.remove(start)
        
        # connect to each neighbor
        for area in [a['neighbor'] for a in start.adjacent]:
            start.connect_to(area)
            unconnected.remove(area)
            frontier.append(area)
            
        while len(unconnected) > 0:
            #print unconnected
            
            changed = False
            for area in frontier[:]:
                frontier.remove(area)
                neighbors = [a['neighbor'] for a in area.adjacent]
                unconnected_neighbors = [n for n in neighbors if n in unconnected]
                                
                # maybe connect to a random neighbor just for kicks
                if dice.one_chance_in(3):
                    area.connect_to(random.choice(neighbors))
                    
                # but always connect to an unconnected neighbor, if there is one
                if unconnected_neighbors:
                    changed = True
                    n = random.choice(unconnected_neighbors)
                    area.connect_to(n)
                    unconnected.remove(n)
                    frontier.append(n)
            
            if not changed and unconnected:
                start = random.choice(unconnected)
                unconnected.remove(start)
                for area in [a['neighbor'] for a in start.adjacent]:
                    start.connect_to(area)
                    if area in unconnected:
                        unconnected.remove(area)
                        frontier.append(area)
                

class Generator(object):
    def __init__(self):
        self.partition_strategy = BSPPartitionStrategy()
        self.connection_strategy = SimpleWebConnectionStrategy()
        self.painter_strategy = RandomPainterStrategy()
        
    def generate(self, width=80, height=80):
        b = board.Board(width, height)
        b.areas = self.partition_strategy.partition(b, 16, 16)
        self.connection_strategy.connect(b.areas)
        self.painter_strategy.paint(b)
        
        return b
        
    
    