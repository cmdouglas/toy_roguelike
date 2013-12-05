import random

from board import board as board_mod
from gameobjects.actors import player
from board.generator import maparea

class Painter(object):
    
    def __init__(self, board, area):
        self.board = board
        self.area = area
    
    def dumps(self):
        board = self.board
        left, top = self.area.ul_pos
        rows = []
        for y in range(top, top + self.area.height):
            row = []
            for x in range(left, left + self.area.width):
                row.append(self.board[(x, y)].draw()[0])
            rows.append("".join(row))
        
        return "\n".join(rows)
        
    def area_meets_requirements(self):
        return True
    
    def get_border(self):
        points = []
        ul_x, ul_y = self.area.ul_pos
        
        for x in range(ul_x, ul_x + self.area.width):
            for y in range(ul_y, ul_y + self.area.height):
                if (x == ul_x or 
                    x == (ul_x + self.area.width - 1) or 
                    y == ul_y or
                    y == (ul_y + self.area.height - 1)):
                    
                    points.append((x, y))
                    
        return points
        
    def place_player(self):
        pos = random.choice(self.area.get_empty_points(self.board))
        self.board.add_object(player.Player(), pos)
        
    def fill(self, ob_type):
        for point in self.area.get_all_points():
            try:
                self.board.add_object(ob_type(), point)
            except board_mod.GameObjectPlacementException:
                continue
    
    def clear(self):
        for point in self.area.get_all_points():
            ob = self.board[point].objects['obstacle']
            if ob:
                self.board.remove_object(ob)
                    
    def draw_corridor(self, start, end, start_dir = None, end_dir=None):
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
            bend = (x_start, y_start + height-1)
            
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
        c1(start, bend)
        c2(bend, end)

    def draw_horizontal_corridor(self, start, end):
        x0, y0 = start
        x1, y1 = end
        x0 = int(x0)
        y0 = int(y0)
        x1 = int(x1)
        y1 = int(y1)
        
        length = x1 - x0
        if length > 0:
            for pos in [(x, y0) for x in range(x0, x0 + length + 1)]:
                tile = self.board[pos]
                self.board.remove_object(tile.objects['obstacle'])
                
        else:
            for pos in [(x, y0) for x in range(x0, x0 + length - 1, -1)]:
                tile = self.board[pos]
                self.board.remove_object(tile.objects['obstacle'])
        
    def draw_vertical_corridor(self, start, end):
        x0, y0 = start
        x1, y1 = end
        x0 = int(x0)
        y0 = int(y0)
        x1 = int(x1)
        y1 = int(y1)
        
        length = y1 - y0
        
        if length > 0:
            for pos in [(x0, y) for y in range(y0, y0 + length +1)]:
                tile = self.board[pos]
                self.board.remove_object(tile.objects['obstacle'])
                
        else:
            for pos in [(x0, y) for y in range(y0, y0 + length - 1, -1)]:
                tile = self.board[pos]
                self.board.remove_object(tile.objects['obstacle'])
        