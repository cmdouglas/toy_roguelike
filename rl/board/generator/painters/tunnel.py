import random

from rl.objects.obstacles import wall
from rl.util import dice, tools
from rl.board.generator.painters import painter


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
        border = self.get_border()
        connections = [c['point'] for c in self.area.connections]
        blocked = set(border)
        blocked -= set(connections)
        
        area_left, area_top = self.area.ul_pos
        
        area_left += 2
        area_top += 2
        
        area_right = int(area_left + (self.area.width-2) / 2)
        area_bottom = int(area_top + (self.area.height-2) / 2)
        
        points = []
        
        for pos in [c['point'] for c in self.area.connections[:-1]]:
            #print "connecting point %s to %s" % (rectangle_center, pos
            points.append(pos)
            points.extend([
                (random.randrange(area_left, area_right), random.randrange(area_top, area_bottom))
                for i in range(dice.d(1, 4))
            ])
        
        points.append(self.area.connections[-1]['point'])
        
        segments = []
        
        for i, point in enumerate(points[:-1]):
            segments.append((point, points[i+1]))
            
        for segment in segments:
            start, end = segment
            try:
                dug = self.smart_draw_corridor(start, end, blocked)
                for p in dug[2:-2]:
                    # try and keep adacent tunnels from being dug
                    blocked += set([p])
                    blocked += set(tools.neighbors(p))

            except:
                dug = self.smart_draw_corridor(start, end, set())

        
        