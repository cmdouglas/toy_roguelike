import logging
from board import board
from board.generator import maparea
from board.generator.painters import painter
from gameobjects import wall


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
        
        logging.debug(self.area)
        logging.debug( self.get_border())
        
        logging.debug("filling border")
        # 1. fill in the border.
        for point in self.get_border():
            self.board.add_object(wall.Wall(), point)
            
        logging.debug("adding doors")
        # 2. connect to the edges.
        for c in self.area.connections:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            border_point = c['point']
            
            if c['side'] in [maparea.TOP, maparea.BOTTOM]:
                end_dir = "vertical"
            else:
                end_dir = 'horizontal'
            
            self.draw_corridor(center, border_point, end_dir=end_dir)
            
        logging.debug("adding pillars")
        # 3. add pillars
        if width > height:
            for x in range(left, right+1):
                if x % 3 == 0:
                    try:
                        top_point = (x, top + v_offset)
                        bottom_point = (x, bottom - v_offset)
                        
                        logging.debug("adding a point at %s" % (top_point,))
                        logging.debug("adding a point at %s" % (bottom_point,))
                        self.board.add_object(wall.Wall(), top_point)
                        self.board.add_object(wall.Wall(), bottom_point)
                        
                    except board.GameObjectPlacementException:
                        pass
                    
        else:
            for y in range(top, bottom+1):
                if y % 3 == 0:
                    try:
                        left_point = (left + h_offset, y)
                        right_point = (right - h_offset, y)
                        
                        logging.debug("adding a point at %s" % (left_point,))
                        logging.debug("adding a point at %s" % (right_point,))
                        self.board.add_object(wall.Wall(), left_point)
                        self.board.add_object(wall.Wall(), right_point)
                    except board.GameObjectPlacementException:
                        pass
        
        logging.debug(self.dumps())
        
        
    def area_meets_requirements(self):
        return self.area.width > 10 and self.area.height > 10