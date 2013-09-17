import random
from util import dice
from gameobjects import player

class Painter(object):
    def get_empty_points(self, board, area):
        return [point for point in area.get_all_points() if not board[point].objects['obstacle']]
        
    def place_player(self, board, area):
        pos = random.choice(self.get_empty_points(board, area))
        board.add_object(player.Player(), pos)
        
    def fill(self, board, area, ob_type):
        for point in area.get_all_points():
            board.add_object(ob_type(), point)
    
    def draw_corridor(self, board, start, end):
        #print "drawing corridor from %s to %s" % (start, end)
        x_start, y_start = start
        x_end, y_end = end
        
        width = x_end - x_start +1
        height = y_end - y_start +1
        # pick horizontal or vertical first
        if (dice.one_chance_in(2)):
            bend = (x_start + width-1, y_start)
            self.draw_horizontal_corridor(board, start, bend)
            self.draw_vertical_corridor(board, bend, end)
            
        else:
            bend = (x_start, y_start + height -1)
            self.draw_vertical_corridor(board, start, bend)
            self.draw_horizontal_corridor(board, bend, end)
        
    def draw_horizontal_corridor(self, board, start, end):
        #print "drawing horizontal corridor from %s to %s" % (start, end)
        x0, y0 = start
        x1, y1 = end
        length = x1 - x0
        if length > 0:
            for pos in [(x, y0) for x in range(x0, x0 + length + 1)]:
                #print "removing object at %s" % (pos,)
                tile = board[pos]
                board.remove_object(tile.objects['obstacle'])
        else:
            for pos in [(x, y0) for x in range(x0, x0 + length - 1, -1)]:
                #print "removing object at %s" % (pos,)
                tile = board[pos]
                board.remove_object(tile.objects['obstacle'])

        
    def draw_vertical_corridor(self, board, start, end):
        #print "drawing vertical corridor from %s to %s" % (start, end)
        x0, y0 = start
        x1, y1 = end
        length = y1 - y0
        
        if length > 0:
            for pos in [(x0, y) for y in range(y0, y0 + length +1)]:
                tile = board[pos]
                #print "removing object at %s" % (pos,)
                board.remove_object(tile.objects['obstacle'])
                
        else:
            for pos in [(x0, y) for y in range(y0, y0 + length - 1, -1)]:
                tile = board[pos]
                ##print "removing object at %s" % (pos,)
                board.remove_object(tile.objects['obstacle'])
        