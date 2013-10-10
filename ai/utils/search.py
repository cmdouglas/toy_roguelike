
class SearchNode(object):
    """Represents a state of a space used for a search.  Initialization 
    requires a dictionary and 2 functions:
    1.  data - a dictionary containing all necessary state information.
    2.  possible_moves(self): returns a list of moves.  A move is an argument in 
    3.  apply_move(self, move):  returns a SearchNode that is the result of the
    passed in move.
    """
    def __init__(self, data, possible_moves, apply_move):
        self.data = data
        self.possible_moves = possible_moves
        self.apply_move = apply_move
        self.move_to_reach = None
        self.parent = None
        self.path_length = None
        
    def __eq__(self, other):
        return self.data == other.data
        
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
            return 1 + self.parent.get_path_length()
        
    def get_path_length(self):
        if not self.path_length:
            self.path_length = self.compute_path_length()
            
        return self.path_length;
            
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
        visited = []
        frontier = [self.start]
        
        def compare(n1, n2):
            c1 = n1.get_path_length() + self.heuristic(self, n1, self.goal)
            c2 = n2.get_path_length() + self.heuristic(self, n2, self.goal)
            
            return cmp(c1, c2)
        
        while frontier:
            current = frontier.pop(0)
            
            if current == self.goal:
                return current.get_path()
                
            for new in current.expand():
                if new in visited:
                    continue
                        
                if new in frontier:
                    continue
                
                if not self.max_depth: 
                    frontier.append(new)
                
                elif new.get_path_length() < self.max_depth:
                    frontier.append(new)
                
            visited.append(current)
            frontier.sort(cmp=compare)
            
        return None
        
    
def find_area_path(board, start, end):
    def possible_moves(node):
        area = node.data['area']
        
        for c in area.connections:
            pass

def find_path(board, start, end, actors_block=False, max_depth=None):
    def possible_moves(node):
        point = node.data['point']
        board = node.data['board']
        moves = []
        
        
        for t in board[point].surrounding():
            
            if actors_block:
                if not t.objects['obstacle'] and not t.objects['actor']:
                    x1, y1 = t.pos
                    x2, y2 = point
                    moves.append((x1 - x2, y1 - y2))
            else:
                if not t.objects['obstacle']:
                    x1, y1 = t.pos
                    x2, y2 = point
                    moves.append((x1 - x2, y1 - y2))
            
        return moves
    
    def apply_move(node, move):
        
        x, y = node.data['point']
        dx, dy = move
        
        return SearchNode({
            'point': (x + dx, y+dy),
            'board': node.data['board']
        }, possible_moves, apply_move)
        
    def heuristic(search, node, goal):
        x2, y2 = goal.data['point']
        x1, y1 = node.data['point']
        
        return abs(x2-x1) + abs(y2-y1)
        
    start_node = SearchNode({
        'point': start,
        'board': board
    }, possible_moves, apply_move)
    
    goal_node = SearchNode({
        'point': end,
        'board': board
    }, possible_moves, apply_move)
    
    return AStarSearch(start_node, goal_node, heuristic, max_depth=max_depth).do_search()