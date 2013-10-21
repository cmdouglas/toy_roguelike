import random
from util import dice
from board.generator.painters import painter
from gameobjects import wall
from gameobjects.actors import goblin

class CavePainter(painter.Painter):
    tags = ['natural', 'underground']
    
    def area_meets_requirements(self):
        return self.area.width >= 10 and self.area.height >= 10
    
    def paint(self):
        def r(point, distance):
            x, y = point
            points = []
            offsets = range(-1*distance, distance+1)
        
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
                if self.board[p].objects['obstacle']:
                    num_walls += 1
                    
            return num_walls
                
        points = [p for p in self.area.get_all_points()]
        
        # 1. randomly fill area with wall tiles
        border = self.get_border()
        
        for point in points:
            if point in border:
                self.board.add_object(wall.Wall(), point)
            elif random.randrange(100) < 40:
                self.board.add_object(wall.Wall(), point)
                                
        # 2.  4 repitions of r(1) == 5 or r(2) == 2
        for i in xrange(4):
            for point in points:
                if walls_in_r(r(point, 1), 1) >= 5:
                    if not self.board[point].objects['obstacle']:
                        self.board.add_object(wall.Wall(), point)
                    
                elif walls_in_r(r(point, 2), 2) <= 2:
                    if not self.board[point].objects['obstacle']:
                        self.board.add_object(wall.Wall(), point)
                else:
                    if self.board[point].objects['obstacle']:
                        
                        self.board.remove_object(self.board[point].objects['obstacle'])
                        
                        
        # 3.  3 repitions of r(1) == 4 
        for i in range(3):            
            for point in points:
                if walls_in_r(r(point, 1), 1) >= 5:
                    if not self.board[point].objects['obstacle']:
                        self.board.add_object(wall.Wall(), point)
                else:
                    if self.board[point].objects['obstacle']:
                        self.board.remove_object(self.board[point].objects['obstacle'])
                    
                    
        # sanity check!  make sure that there's room for the goblins!
        if len(self.area.get_empty_points(self.board)) < 10:
            self.clear()
            return self.paint()
        
        # 4.  Add 1-9 goblins
        for i in range((dice.d(2, 5) - 1)):
            point = random.choice(self.area.get_empty_points(self.board))
            self.board.add_object(goblin.Goblin(), point)
            
        for point in points:
            if point in border and not self.board[point].objects['obstacle']:
                self.board.add_object(wall.Wall(), point)
                        
        #5.  Connect to the area entrances
        point = random.choice(self.area.get_empty_points(self.board))
        
        for pos in [c['point'] for c in self.area.connections]:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            self.draw_corridor(point, pos)
        
        