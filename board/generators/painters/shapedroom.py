import random

from util import shape
from board.generators.painters import painter
from gameobjects import smoothwall

class RectangularRoomPainter(painter.Painter):
    def paint(self, board, area):
        
        area_left, area_top = area.ul_pos
        rectangle_width = random.randrange(area.width / 2, area.width)
        rectangle_height = random.randrange(area.height / 2, area.height)
        
        horizontal_offset = random.randrange(area.width - rectangle_width)
        vertical_offset = random.randrange(area.height - rectangle_height)
        
        rectangle_center = (
            area_left + horizontal_offset + rectangle_width / 2,
            area_top + vertical_offset + rectangle_height / 2)
            
        r = shape.Rectangle(rectangle_center, rectangle_width, rectangle_height)
        
        for pos in r.points:
            tile = board[pos]
            board.remove_object(tile.objects['obstacle'])
        
        for pos in [c['point'] for c in area.connections]:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            self.draw_corridor(board, rectangle_center, pos)
