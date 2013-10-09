import random

from util import dice
from gameobjects import player
from board import board

class Painter(object):
    
    def dumps(self, board, area):
        left, top = area.ul_pos
        rows = []
        for y in range(top, top + area.height):
            row = []
            for x in range(left, left + area.width):
                row.append(board[(x, y)].draw()[0])
            rows.append("".join(row))
        
        return "\n".join(rows)
        
    def area_meets_requirements(self, area):
        return True
    
    def get_border(self, area):
        points = []
        ul_x, ul_y = area.ul_pos
        
        for x in range(ul_x, ul_x + area.width - 1):
            for y in range(ul_y, ul_y + area.height - 1):
                if (x == ul_x or 
                    x == (ul_x + area.width -1) or 
                    y == ul_y or
                    y == (ul_y + area.height - 1)):
                    
                    points.append((x, y))
                    
        return points
        
    def place_player(self, board, area):
        pos = random.choice(area.get_empty_points(board))
        board.add_object(player.Player(), pos)
        
    def fill(self, board, area, ob_type):
        for point in area.get_all_points():
            try:
                board.add_object(ob_type(), point)
            except board.GameObjectPlacementException:
                continue
    
    def draw_corridor(self, board, start, end, start_dir = None, end_dir=None):
        #print "drawing corridor from %s to %s" % (start, end)
        x_start, y_start = start
        x_end, y_end = end
        
        width = x_end - x_start +1
        height = y_end - y_start +1
        # pick horizontal or vertical first
        
        if start_dir == "horizontal" or end_dir == 'vertical':
            bend = (x_start + width-1, y_start)
            order = [self.draw_horizontal_corridor,
                     self.draw_vertical_corridor]
            
        elif start_dir == "vertical" or end_dir == 'horizontal':
            
            order = [self.draw_vertical_corridor,
                     self.draw_horizontal_corridor]
        else:
            order = [self.draw_horizontal_corridor,
                     self.draw_vertical_corridor]
            
            random.shuffle(order)
            
            if order[0] == self.draw_horizontal_corridor:
                bend = (x_start + width-1, y_start)
            else:
                bend = (x_start, y_start + height -1)
            
        c1, c2 = order
        c1(board, start, bend)
        c2(board, bend, end)

    def draw_horizontal_corridor(self, board, start, end):
        x0, y0 = start
        x1, y1 = end
        length = x1 - x0
        if length > 0:
            for pos in [(x, y0) for x in range(x0, x0 + length + 1)]:
                tile = board[pos]
                board.remove_object(tile.objects['obstacle'])
                
        else:
            for pos in [(x, y0) for x in range(x0, x0 + length - 1, -1)]:
                tile = board[pos]
                board.remove_object(tile.objects['obstacle'])
        
    def draw_vertical_corridor(self, board, start, end):
        x0, y0 = start
        x1, y1 = end
        length = y1 - y0
        
        if length > 0:
            for pos in [(x0, y) for y in range(y0, y0 + length +1)]:
                tile = board[pos]
                board.remove_object(tile.objects['obstacle'])
                
        else:
            for pos in [(x0, y) for y in range(y0, y0 + length - 1, -1)]:
                tile = board[pos]
                board.remove_object(tile.objects['obstacle'])
        