import random

from rl.entities.obstacles import wall
from rl.util import tools
from rl.board.generator.painters import Painter


class CavePainter(Painter):
    tags = ['natural', 'underground']

    @classmethod
    def region_meets_requirements(cls, region):
        return region.shape.width >= 10 and region.shape.height >= 10
    
    def paint(self):
        def r(point, distance):
            x, y = point
            points = []
            offsets = list(range(-1*distance, distance+1))
        
            for x_offset in offsets:
                for y_offset in offsets:
                    p = (x + x_offset, y+y_offset)
                    if p in self.region.shape.points:
                        points.append(p)
        
            return points
            
        def walls_in_r(r, distance):
            num_walls = 0
            
            # count "edge" tiles as walls
            num_tiles = (distance*2 + 1)**2
            num_walls += num_tiles - len(r)
            
            for p in r:
                if self.board[p].obstacle:
                    num_walls += 1
                    
            return num_walls
                
        points = [p for p in self.region.shape.points]
        
        # 1. randomly fill region with wall tiles
        border = self.region.shape.border
        
        for point in points:
            if point in border and not self.board[point].obstacle:
                self.board.add_entity(wall.Wall(), point)
            elif random.randrange(100) < 40:
                self.board.add_entity(wall.Wall(), point)
                                
        # 2.  4 repitions of r(1) == 5 or r(2) == 2
        for i in range(4):
            for point in points:
                if walls_in_r(r(point, 1), 1) >= 5:
                    if not self.board[point].obstacle:
                        self.board.add_entity(wall.Wall(), point)
                    
                elif walls_in_r(r(point, 2), 2) <= 2:
                    if not self.board[point].obstacle:
                        self.board.add_entity(wall.Wall(), point)
                else:
                    if self.board[point].obstacle and not point in border:
                        
                        self.board.remove_entity(self.board[point].obstacle)
                        
                        
        # 3.  3 repitions of r(1) == 4 
        for i in range(3):            
            for point in points:
                if walls_in_r(r(point, 1), 1) >= 5:
                    if not self.board[point].obstacle:
                        self.board.add_entity(wall.Wall(), point)
                else:
                    if self.board[point].obstacle and not point in border:
                        self.board.remove_entity(self.board[point].obstacle)


        for border_point in border:
            if not self.board[border_point].obstacle:
                self.board.add_entity(wall.Wall(), border_point)

        #make sure zones are connected
        zones = self.find_zones()
        if len(zones) > 1:
            for zone1, zone2 in tools.pairwise(zones):
                p1 = random.choice(list(zone1))
                p2 = random.choice(list(zone2))

                self.smart_draw_corridor(p1, p2, [])
                        
        # 5.  Connect to the region entrances
        empty_points = self.region.empty_points()
        if not empty_points:
            self.clear()
            return self.paint()

        point = random.choice(empty_points)
        
        for access_point in self.region.connections:
            if self.board[access_point].obstacle:
                self.board.remove_entity(self.board[access_point].obstacle)
            self.smart_draw_corridor(access_point, point)