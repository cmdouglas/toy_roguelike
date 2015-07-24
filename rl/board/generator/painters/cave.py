import random

from rl.entities.obstacles import wall
from rl.util import tools
from rl.board.generator.painters import Painter
from rl.board.generator import maparea
from rl.entities.actors import goblin


class CavePainter(Painter):
    tags = ['natural', 'underground']
    
    def area_meets_requirements(self):
        return self.area.width >= 10 and self.area.height >= 10
    
    def paint(self):
        def r(point, distance):
            x, y = point
            points = []
            offsets = list(range(-1*distance, distance+1))
        
            for x_offset in offsets:
                for y_offset in offsets:
                    p = (x + x_offset, y+y_offset)
                    if (self.area.contains_point(p)):
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
                
        points = [p for p in self.area.get_all_points()]
        
        # 1. randomly fill area with wall tiles
        border = self.get_border()
        
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
                        
        # 5.  Connect to the area entrances
        empty_points = self.area.get_empty_points()
        if not empty_points:
            self.clear()
            return self.paint()

        point = random.choice(empty_points)
        
        for c in self.area.connections:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            border_point = c['point']
            
            if c['side'] in [maparea.TOP, maparea.BOTTOM]:
                end_dir = "vertical"
            else:
                end_dir = 'horizontal'
            
            self.draw_corridor(point, border_point, end_dir=end_dir)
        
        