import random

from rl.util import dice
from rl.util import partition
from rl.board.generator.painters import painter
from rl.board.generator import maparea
from rl.entities.obstacles import smoothwall, door


class RoomClusterPainter(painter.Painter):
    
    def __init__(self, board, area):
        super().__init__(board, area)
        self.board = board
        self.area = area
        self.min_room_height = 5
        self.min_room_width = 5
        
    def paint(self):
        connecting_points = [c['point'] for c in self.area.connections]
        for point in self.area.border():
            if point in connecting_points:
                self.board.add_entity(door.Door(), point)
            else:
                self.board.add_entity(smoothwall.SmoothWall(), point)

        areas = self.subpartition()
        self.connect(areas)

        for area in areas:
            self.paint_subarea(area)


    def area_meets_requirements(self):
        return self.area.width > 10 and self.area.height > 10
        
    def subpartition(self):
        part = partition.Partition(self.area.ul_pos, self.area.width, self.area.height)
        
        ps = part.subpartition_bsp(5, 5)

        areas = [maparea.MapArea(p, self.board) for p in ps]
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
        x0, y0 = sub.ul_pos
        connecting_points = [c['point'] for c in sub.connections]
        for x in range(x0, x0+sub.width):
            p = (x, y0)
            if p in connecting_points:
                try:
                    self.board.add_entity(door.Door(), p)
                except:
                    pass

            else:
                try:
                    self.board.add_entity(smoothwall.SmoothWall(), p)
                except:
                    pass

        for y in range(y0, y0+sub.height):
            p = (x0, y)
            if p in connecting_points:
                try:
                    self.board.add_entity(door.Door(), p)
                except:
                    pass

            else:
                try:
                    self.board.add_entity(smoothwall.SmoothWall(), p)
                except:
                    pass





        
    