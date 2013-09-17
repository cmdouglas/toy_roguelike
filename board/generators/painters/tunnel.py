import random
from util import dice
from board.generators.painters import painter

class SimpleTunnelPainter(painter.Painter):
    def paint(self, board, area):
        area_left, area_top = area.ul_pos
        
        area_left += 2
        area_top += 2
        
        center = (area_left + (area.width-2) / 2, area_top + (area.height-2) / 2)
        
        for pos in [c['point'] for c in area.connections]:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            self.draw_corridor(board, center, pos)
            
class SnakeyTunnelPainter(painter.Painter):
    def paint(self, board, area):
        area_left, area_top = area.ul_pos
        
        area_left += 2
        area_top += 2
        
        area_right = area_left + (area.width-2) / 2
        area_bottom = area_top + (area.height-2) / 2
        
        points = []
        
        for pos in [c['point'] for c in area.connections[:-1]]:
            #print "connecting point %s to %s" % (rectangle_center, pos
            points.append(pos)
            points.extend([
                (random.randrange(area_left, area_right), random.randrange(area_top, area_bottom))
                for i in xrange(dice.d(1, 3))
            ])
        
        points.append(area.connections[-1]['point'])
        
        segments = []
        
        for i, point in enumerate(points[:-1]):
            segments.append((point, points[i+1]))
            
        for segment in segments:
            start, end = segment
            self.draw_corridor(board, start, end)
        
        