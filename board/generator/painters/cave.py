import random
from util import dice
from board.generator.painters import painter
from gameobjects import wall

class CavePainter(painter.Painter):
    def area_meets_requirements(self, area):
        return area.width > 10 and area.height > 10
    
    def paint(self, board, area):
        def r(point, distance):
            x, y = point
            points = []
            offsets = range(-1*distance, distance+1)
        
            for x_offset in offsets:
                for y_offset in offsets:
                    p = (x + x_offset, y+y_offset)
                    if (area.contains_point(p)):
                            points.append(p)
        
            return points
            
        def walls_in_r(board, r, distance):
            num_walls = 0
            
            # count "edge" tiles as walls
            num_tiles = (distance*2 + 1)**2
            num_walls += num_tiles - len(r)
            
            for p in r:
                if board[p].objects['obstacle']:
                    num_walls += 1
                    
            return num_walls
                
        points = [p for p in area.get_all_points()]
        
        # 1. randomly fill area with wall tiles
        for point in points:
            if random.randrange(100) < 40:
                board.add_object(wall.Wall(), point)
                                
        # 2.  4 repitions of r(1) == 5 or r(2) == 2
        for i in xrange(4):
            for point in points:
                num_walls = walls_in_r(board, r(point, 1), 1)
                if walls_in_r(board, r(point, 1), 1) >= 5:
                    if not board[point].objects['obstacle']:
                        board.add_object(wall.Wall(), point)
                    
                elif walls_in_r(board, r(point, 2), 2) <= 2:
                    if not board[point].objects['obstacle']:
                        board.add_object(wall.Wall(), point)
                else:
                    if board[point].objects['obstacle']:
                        
                        board.remove_object(board[point].objects['obstacle'])
                        
                        
        # 3.  3 repitions of r(1) == 4 
        for i in range(3):            
            for point in points:
                num_walls = walls_in_r(board, r(point, 1), 1)
                if walls_in_r(board, r(point, 1), 1) >= 5:
                    if not board[point].objects['obstacle']:
                        board.add_object(wall.Wall(), point)
                else:
                    if board[point].objects['obstacle']:
                        board.remove_object(board[point].objects['obstacle'])
                        
                        
        #4.  Connect to the area entrances
        point = random.choice(self.get_empty_points(board, area))
        
        for pos in [c['point'] for c in area.connections]:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            self.draw_corridor(board, point, pos)
        
        