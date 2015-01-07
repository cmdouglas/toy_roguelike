from rl.board import tile
from rl.board.generator import maparea
from rl.board.generator.painters import painter
from rl.entities.obstacles import wall


class GreatHallPainter(painter.Painter):
    def paint(self):
        left, top = self.area.ul_pos
        width = self.area.width - 4
        height = self.area.height -4
        
        center = (int(left + self.area.width / 2), int(top + self.area.height / 2))
        
        top += 2
        left += 2
        bottom = top + height
        right = left + width
        
        h_offset = int(width / 6)
        v_offset = int(height / 6)
        
        # 1. fill in the border.
        for point in self.get_border():
            self.board.add_entity(wall.Wall(), point)
            
        # 2. connect to the edges.
        for c in self.area.connections:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            border_point = c['point']
            
            if c['side'] in [maparea.TOP, maparea.BOTTOM]:
                end_dir = "vertical"
            else:
                end_dir = 'horizontal'
            
            self.draw_corridor(center, border_point, end_dir=end_dir)
            
        # 3. add pillars
        if width > height:
            l, r = left + 1, right -2
            while l <= r:
                try:
                    
                    top_point = (l, top + v_offset)
                    bottom_point = (l, bottom - (v_offset + 1))
                    
                    self.board.add_entity(wall.Wall(), top_point)
                    self.board.add_entity(wall.Wall(), bottom_point)
                    
                    top_point = (r, top + v_offset)
                    bottom_point = (r, bottom - (v_offset + 1))

                    self.board.add_entity(wall.Wall(), top_point)
                    self.board.add_entity(wall.Wall(), bottom_point)
                    
                except tile.EntityPlacementException:
                    pass
                    
                l += 3
                r -= 3
                    
        else:
            t, b = top + 1, bottom -2
            while t <= b:
                try:
                    left_point = (left + h_offset, t)
                    right_point = (right - (h_offset + 1), t)
                    
                    self.board.add_entity(wall.Wall(), left_point)
                    self.board.add_entity(wall.Wall(), right_point)
                    
                    left_point = (left + h_offset, b)
                    right_point = (right - (h_offset + 1), b)
                    
                    self.board.add_entity(wall.Wall(), left_point)
                    self.board.add_entity(wall.Wall(), right_point)
                        
                except tile.EntityPlacementException:
                    pass
                    
                t += 3
                b -= 3        
        
    def area_meets_requirements(self):
        return self.area.width > 10 and self.area.height > 10