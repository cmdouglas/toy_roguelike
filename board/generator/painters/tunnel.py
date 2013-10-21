import random
from util import dice
from board.generator.painters import painter
from gameobjects import wall

class TunnelPainter(painter.Painter):
    def area_meets_requirements(self):
        # no dead end tunnels
        return len(self.area.connections) >= 2

class SimpleTunnelPainter(TunnelPainter):
    def paint(self):
        self.fill(wall.Wall)
        
        area_left, area_top = self.area.ul_pos
        
        area_left += 2
        area_top += 2
        
        center = (area_left + (self.area.width-2) / 2, area_top + (self.area.height-2) / 2)
        
        for pos in [c['point'] for c in self.area.connections]:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            self.draw_corridor(center, pos)
            
class SnakeyTunnelPainter(TunnelPainter):
    def paint(self):
        self.fill(wall.Wall)
        
        area_left, area_top = self.area.ul_pos
        
        area_left += 2
        area_top += 2
        
        area_right = area_left + (self.area.width-2) / 2
        area_bottom = area_top + (self.area.height-2) / 2
        
        points = []
        
        for pos in [c['point'] for c in self.area.connections[:-1]]:
            #print "connecting point %s to %s" % (rectangle_center, pos
            points.append(pos)
            points.extend([
                (random.randrange(area_left, area_right), random.randrange(area_top, area_bottom))
                for i in xrange(dice.d(1, 4))
            ])
        
        points.append(self.area.connections[-1]['point'])
        
        segments = []
        
        for i, point in enumerate(points[:-1]):
            segments.append((point, points[i+1]))
            
        for segment in segments:
            start, end = segment
            self.draw_corridor(start, end)
        
        