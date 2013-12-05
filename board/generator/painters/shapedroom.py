import random

from util import shape
from util import dice
from board.generator.painters import painter
from board.generator import maparea
from gameobjects import wall
from gameobjects import smoothwall
from gameobjects.items import potion

class ShapedRoomPainter(painter.Painter):
    def get_bounding_box(self):
        area_left, area_top = self.area.ul_pos

        area_left += 2
        area_top += 2
                
        width = self.area.width - 4
        height = self.area.height - 4
        
        rectangle_width = random.randrange(int(width / 2), width)
        rectangle_height = random.randrange(int(height / 2), height)
        
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
        
    def area_meets_requirements(self):
        return self.area.width > 8 and self.area.height > 8

class RectangularRoomPainter(ShapedRoomPainter):
    def paint(self):
        self.fill(wall.Wall)
        center, width, height = self.get_bounding_box()
        
        rectangle = shape.Rectangle(center, width, height)
        
        for pos in rectangle.points:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            
        for pos in rectangle.border:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            self.board.add_object(smoothwall.SmoothWall(), pos)
    
        for c in self.area.connections:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            border_point = c['point']
            
            if c['side'] in [maparea.TOP, maparea.BOTTOM]:
                end_dir = "vertical"
            else:
                end_dir = 'horizontal'
            
            self.draw_corridor(center, border_point, end_dir=end_dir)
            
        self.board[center].add_item(potion.HealingPotion())
            
class CircularRoomPainter(ShapedRoomPainter):
    def paint(self):
        self.fill(wall.Wall)
        center, width, height = self.get_bounding_box()
        
        circle = shape.Circle(center, min(width, height)/2)
        
        for pos in circle.points:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            
        for pos in circle.border:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            self.board.add_object(smoothwall.SmoothWall(), pos)
    
        for c in self.area.connections:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            border_point = c['point']
            
            if c['side'] in [maparea.TOP, maparea.BOTTOM]:
                end_dir = "vertical"
            else:
                end_dir = 'horizontal'
            
            self.draw_corridor(center, border_point, end_dir=end_dir)
            
        self.board[center].add_item(potion.HealingPotion())
            
            
class EllipticalRoomPainter(ShapedRoomPainter):
    def paint(self):
        self.fill(wall.Wall)
        
        center, width, height = self.get_bounding_box()
        
        ellipse = shape.Ellipse(center, width/2, height/2)
        
        for pos in ellipse.points:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            
        for pos in ellipse.border:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            self.board.add_object(smoothwall.SmoothWall(), pos)
    
        for c in self.area.connections:
            #print "connecting point %s to %s" % (rectangle_center, pos)
            border_point = c['point']
            
            if c['side'] in [maparea.TOP, maparea.BOTTOM]:
                end_dir = "vertical"
            else:
                end_dir = 'horizontal'
            
            self.draw_corridor(center, border_point, end_dir=end_dir)

        self.board[center].add_item(potion.HealingPotion())
        

