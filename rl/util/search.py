import heapq
import logging

from functools import total_ordering

logger = logging.getLogger('rl')

@total_ordering
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
            
        return self.path_length
            
    def get_path_depth(self):
        if not self.path_depth:
            self.path_depth = self.compute_path_depth()
            
        return self.path_depth
            
    def get_path(self):
        moves = []
        
        n = self
        while n.parent:
            moves.append(n.move_to_reach)
            n = n.parent
            
        return [m for m in reversed(moves)]

    def __str__(self):
        return str(self.data)

    def __lt__(self, other):
        # for the most part, these will be compared based on their g+h values.  this is a tie-breaker for when those
        # are equal
        return self.id(self) < other.id(other)
    

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

        def sortkey(node):
            if not node.h:
                node.h = self.heuristic(self, node, self.goal)
            
            return node.get_path_length() + node.h

        frontier = [(sortkey(self.start), self.start)]
        heapq.heapify(frontier)
        fset = set()
        fset.add(self.start.id(self.start))

        # logger.debug('SEARCH START')
        # logger.debug('start:' + str(self.start))
        # logger.debug('goal:' + str(self.goal))
        # logger.debug('frontier: ' + str(frontier))

        while frontier:
            # logger.debug('frontier:' + str(frontier))
            # logger.debug('visited:' + str(visited))
            _, current = heapq.heappop(frontier)
            
            if current == self.goal:
                # logger.debug('GOAL FOUND')
                return current.get_path()
                
            for new in current.expand():
                # logger.debug('expand found: '+ str(new))
                if (new.id(new) in visited and
                    new.get_path_length() >= visited[new.id(new)].get_path_length()):
                    # logger.debug('shorter path to here already found')
                    continue
                        
                if new.id(new) in fset:
                    # logger.debug('already in frontier')
                    continue
                
                if not self.max_depth:
                    # logger.debug('adding to frontier')
                    heapq.heappush(frontier, (sortkey(new), new))
                    fset.add(new.id(new))

                elif new.get_path_depth() < self.max_depth:
                    # logger.debug('adding to frontier')
                    heapq.heappush(frontier, (sortkey(new), new))
                    fset.add(new.id(new))

                # logger.debug('adding to visited.')
                visited[new.id(new)] = new

        return None

def find_path(board, start, end,
              actors_block=False,
              only_known_points=False,
              doors_block=True,
              max_depth=None):
    
    def id(node):
        return node.data['point']
        
    def possible_moves(node):
        point = node.data['point']
        board = node.data['board']
        moves = []
        
        
        for t in board[point].neighbors():


            if actors_block and t.actor and t.pos != end:
                continue

            if doors_block and t.is_closed_door():
                continue

            if only_known_points and not (t.visible or t.has_been_seen):
                continue

            if t.blocks_movement() and t.terrain and not t.is_closed_door():
                continue

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