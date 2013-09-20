import random

from util import shape
from board.generator.painters import painter
from gameobjects import wall
from gameobjects import smoothwall

class ShapedRoomPainter(painter.Painter):
    def get_bounding_box(self, board, area):
        area_left, area_top = area.ul_pos

        area_left += 2
        area_top += 2
                
        width = area.width - 4
        height = area.height - 4
        
        rectangle_width = random.randrange(width / 2, width)
        rectangle_height = random.randrange(height / 2, height)
        
        horizontal_offset = 0
        vertical_offset = 0
        
        if width - rectangle_width > 1:
            horizontal_offset = random.randrange(width - rectangle_width)
        
        if height - rectangle_height > 1:
            vertical_offset = random.randrange(height - rectangle_height)
        
        rectangle_center = (
            area_left + horizontal_offset + rectangle_width / 2,
            area_top + vertical_offset + rectangle_height / 2)
            
        return (rectangle_center, rectangle_width, rectangle_height)
        
    def area_meets_requirements(self, area):
        return area.width > 8 and area.height > 8

class RectangularRoomPainter(ShapedRoomPainter):
    def paint(self, board, area):
        self.fill(board, area, wall.Wall)
        center, width, height = self.get_bounding_box(board, area)
        
        rectangle = shape.Rectangle(center, width, height)
        
        for pos in rectangle.points:
            tile = board[pos]
            board.remove_object(tile.objects['obstacle'])
            
        for pos in rectangle.border:
            tile = board[pos]
            board.remove_object(tile.objects['obstacle'])
            board.add_object(smoothwall.SmoothWall(), pos)
    
        for pos in [c['point'] for c in area.connections]:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            self.draw_corridor(board, center, pos)
            
class CircularRoomPainter(ShapedRoomPainter):
    def paint(self, board, area):
        self.fill(board, area, wall.Wall)
        center, width, height = self.get_bounding_box(board, area)
        
        circle = shape.Circle(center, min(width, height)/2)
        
        for pos in circle.points:
            tile = board[pos]
            board.remove_object(tile.objects['obstacle'])
            
        for pos in circle.border:
            tile = board[pos]
            board.remove_object(tile.objects['obstacle'])
            board.add_object(smoothwall.SmoothWall(), pos)
    
        for pos in [c['point'] for c in area.connections]:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            self.draw_corridor(board, center, pos)
            
class EllipticalRoomPainter(ShapedRoomPainter):
    def paint(self, board, area):
        self.fill(board, area, wall.Wall)
        
        center, width, height = self.get_bounding_box(board, area)
        
        ellipse = shape.Ellipse(center, width/2, height/2)
        
        for pos in ellipse.points:
            tile = board[pos]
            board.remove_object(tile.objects['obstacle'])
            
        for pos in ellipse.border:
            tile = board[pos]
            board.remove_object(tile.objects['obstacle'])
            board.add_object(smoothwall.SmoothWall(), pos)
    
        for pos in [c['point'] for c in area.connections]:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            self.draw_corridor(board, center, pos)


