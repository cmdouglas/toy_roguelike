import random

from rl import globals as G
from rl.ai.utils import search
from rl.util import tools
from rl.board import board as board_mod
from rl.board import tile

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
        
    def fill(self, ob_type):
        for point in self.area.get_all_points():
            try:
                self.board.add_object(ob_type(), point)
            except tile.GameObjectPlacementException:
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

    def smart_draw_corridor(self, start, end, blocked):
        """uses an A* search to find a corridor from start to end that does not cross any points in blocked"""

        def id(node):
            return node.data['point']

        def possible_moves(node):
            point = node.data['point']
            moves = []

            for p in tools.adjacent(point):
                if self.area.contains_point(p) and p not in blocked:
                    moves.append(p)

            return moves

        def apply_move(node, move):
            path_cost = 1000

            return search.SearchNode({
                'point': move,
                'path_cost': path_cost
            }, id, possible_moves, apply_move)

        def heuristic(search, node, goal):
            x2, y2 = goal.data['point']
            x1, y1 = node.data['point']

            return (abs(x2-x1) + abs(y2-y1)) * 1000

        start_node = search.SearchNode({
            'point': start,
        }, id, possible_moves, apply_move)

        goal_node = search.SearchNode({
            'point': end,
        }, id, possible_moves, apply_move)

        points = search.AStarSearch(start_node, goal_node, heuristic).do_search()

        if points:
            for point in points:
                self.board.remove_object(self.board[point].objects['obstacle'])

        