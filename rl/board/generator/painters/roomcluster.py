import random

from rl import globals as G
from rl.util import dice
from rl.util import partition
from rl.board.generator.painters import painter


class RoomClusterPainter(painter.Painter):
    
    def __init__(self, area):
        self.area = area
        self.min_room_height = 5
        self.min_room_width = 5
        
    def paint(self):
        pass
        
    def area_meets_requirements(self, area):
        return area.width >= 10 and area.height >= 10
        
    def subpartition(self):
        part = partition.Partition(self.area.ul_corner, self.area.width, self.area.height)
        
        ps = part.subpartition_bsp(5, 5)
        
        areas = [G.MapArea(p) for p in ps]
        for area in areas:
            area.find_neighbors(areas)
        
        return areas
        
    def connect(self, subareas):
        unconnected = subareas[:]
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
    
    def paint_subarea(self, sub):
        if sub.contains_point():
            pass
        
    