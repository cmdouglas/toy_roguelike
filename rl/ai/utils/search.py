    
class SearchNode(object):
    """Represents a state of a space used for a search.  Initialization 
    requires a dictionary and 3 functions:
    1.  data - a dictionary containing all necessary state information.
    3.  id(node): a function that returns an identifier representing the state
    2.  possible_moves(self): returns a list of moves.  A move is an argument in 
    3.  apply_move(self, move):  returns a SearchNode that is the result of the
    passed in move.
    """
    
    __slots__ = [
        'data',
        'id',
        'possible_moves',
        'apply_move',
        'move_to_reach',
        'parent',
        'path_length',
        'path_depth',
        'h'
    ]
    
    def __init__(self, data, id, possible_moves, apply_move):
        self.data = data
        self.id = id
        self.possible_moves = possible_moves
        self.apply_move = apply_move
        self.move_to_reach = None
        self.parent = None
        self.path_length = None
        self.path_depth = None
        self.h = None
        
    def __eq__(self, other):
        return self.id(self) == other.id(other)
        
    def expand(self):
        nodes = []
        moves = self.possible_moves(self)
        for move in moves:
            node = self.apply_move(self, move)
            node.parent = self
            node.move_to_reach = move
            nodes.append(node)
            
        return nodes
        
    def compute_path_length(self):
        if not self.parent:
            return 0
        else:
            return self.data.get('path_cost', 1) + self.parent.get_path_length()
            
    def compute_path_depth(self):
        if not self.parent:
            return 0
        else:
            return 1 + self.parent.get_path_depth()
        
    def get_path_length(self):
        if not self.path_length:
            self.path_length = self.compute_path_length()
            
        return self.path_length;
            
    def get_path_depth(self):
        if not self.path_depth:
            self.path_depth = self.compute_path_depth()
            
        return self.path_depth;
            
    def get_path(self):
        moves = []
        
        n = self
        while n.parent:
            moves.append(n.move_to_reach)
            n = n.parent
            
        return [m for m in reversed(moves)]
        
    
        

class AStarSearch(object):
    """An A* search. Initialization requires:
    1.  start:  A SearchNode representing the initial state
    2.  goal: a SearchNode representing the goal state
    3.  heuristic(self, node, goal):  a function that takes a SearchNode and returns
    an integer, representing an estimated number of moves from state to goal.
    """
    def __init__(self, start, goal, heuristic, max_depth=None):
        self.start = start
        self.goal = goal
        self.heuristic = heuristic
        self.max_depth = max_depth
        
    def do_search(self):
        visited = {}
        frontier = [self.start]
        
        def sortkey(node):
            if not node.h:
                node.h = self.heuristic(self, node, self.goal)
            
            return node.get_path_length() + node.h
        
        while frontier:
            current = frontier.pop(0)
            
            if current == self.goal:
                return current.get_path()
                
            for new in current.expand():
                if (new.id(new) in visited and
                    new.get_path_length() >= visited[new.id(new)].get_path_length()):
                    continue
                        
                if new in frontier:
                    continue
                
                if not self.max_depth: 
                    frontier.append(new)
                
                elif new.get_path_depth() < self.max_depth:
                    frontier.append(new)
                
                visited[new.id(new)] = new
            frontier.sort(key=sortkey)
            
        return None
        
    
def find_area_path(board, start, end):
    def possible_moves(node):
        area = node.data['area']
        
        for c in area.connections:
            pass

def find_path(board, start, end,
              actors_block=False,
              doors_block=True,
              max_depth=None):
    
    def id(node):
        return node.data['point']
        
    def possible_moves(node):
        point = node.data['point']
        board = node.data['board']
        moves = []
        
        
        for t in board[point].surrounding():
            
            # not counting an actor on the goal point as blocking.
            if actors_block and t.pos != end:
                if not t.entities['obstacle'] and not t.entities['actor']:
                    x1, y1 = t.pos
                    x2, y2 = point
                    moves.append((x1 - x2, y1 - y2))
            else:
                obstacle = t.entities['obstacle']
                if obstacle is None or ((not doors_block) and obstacle.is_door):
                    x1, y1 = t.pos
                    x2, y2 = point
                    moves.append((x1 - x2, y1 - y2))
            
        return moves
    
    def apply_move(node, move):
        
        x, y = node.data['point']
        dx, dy = move
        
        path_cost = 1000
        if (dx != 0 and dy != 0):
            # ~sqrt(2)*1000 for diagonal moves
            path_cost = 1414
            
        
        return SearchNode({
            'point': (x + dx, y+dy),
            'board': node.data['board'],
            'path_cost': path_cost
        }, id, possible_moves, apply_move)
        
    def heuristic(search, node, goal):
        x2, y2 = goal.data['point']
        x1, y1 = node.data['point']
        
        return (abs(x2-x1) + abs(y2-y1)) * 1000
        
    start_node = SearchNode({
        'point': start,
        'board': board
    }, id, possible_moves, apply_move)
    
    goal_node = SearchNode({
        'point': end,
        'board': board
    }, id, possible_moves, apply_move)
    
    return AStarSearch(start_node, goal_node, heuristic, max_depth=max_depth).do_search()