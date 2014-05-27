import math

from rl import globals as G
from rl.ai.utils import search

def move_towards(actor1, actor2):
    board = G.board
    self_pos = actor1.tile.pos
    other_pos = actor2.tile.pos
    
    path = search.find_path(board, self_pos, other_pos)
    
    if path:
        actor1.move(path[0])
        
def move_towards_player(actor):
    return move_towards(actor, G.player)
    
def is_home(actor):
    pass
    
def go_home(actor):
    pass
    
def can_see_player(actor):
    return can_see(actor, G.player)
    
def can_see(actor1, actor2):
    board=G.board
    
    def get_direction(p_from, p_to):
        x1, y1 = p_from
        x2, y2 = p_to
        
        dx = x2 - x1
        dy = y2 - y1
        
        distance = math.sqrt(dx ** 2 + dy ** 2)

        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        
        return (dx, dy)
    
    self_pos = actor1.tile.pos
    other_pos = actor2.tile.pos
    
    p = self_pos
    
    x1, y1 = self_pos
    x2, y2 = other_pos
    
    if (abs(x2-x1) > actor1.sight_radius or abs(y2-y1 > actor2.sight_radius)):
        return False
    
    while p != other_pos:
        direction = get_direction(p, other_pos)
        x, y = p
        dx, dy = direction
        
        p = (x + dx, y + dy)
        
        if board[p].blocks_vision():
            return False
    
    return True