import random
import math

from rl.util import geometry, search
from rl.world.board import tile


class Painter(object):

    def __init__(self, board, region):
        self.board = board
        self.region = region

    @classmethod
    def region_meets_requirements(cls, region):
        return True

    def fill(self, ent_type):
        for point in self.region.shape.points:
            try:
                self.board.add_entity(ent_type(), point)
            except tile.EntityPlacementException:
                continue

    def clear(self):
        for point in self.region.shape.points:
            ent = self.board[point].terrain
            if ent:
                self.board.remove_entity(ent)

    def smart_draw_corridor(self, start, end, blocked=None, costs=None):
        """uses an A* search to find a corridor from start to end that does not cross any points in blocked"""
        if not blocked:
            blocked = set()

        if not costs:
            costs = {}

        if start == end:
            return []

        def id(node):
            return node.data['point']

        def possible_moves(node):
            point = node.data['point']
            moves = []

            for p in geometry.adjacent(point):
                if p in self.region.shape.points and p not in blocked:
                    moves.append(p)

            return moves

        def apply_move(node, move):
            if costs:
                path_cost = costs.get(move, 1000)
            else:
                path_cost = 1000

            return search.SearchNode({
                'point': move,
                'path_cost': path_cost
            }, id, possible_moves, apply_move)

        def heuristic(search, node, goal):
            x2, y2 = goal.data['point']
            x1, y1 = node.data['point']

            return int(math.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2)) * 1000

        start_node = search.SearchNode({
            'point': start,
        }, id, possible_moves, apply_move)

        goal_node = search.SearchNode({
            'point': end,
        }, id, possible_moves, apply_move)

        points = search.AStarSearch(start_node, goal_node, heuristic).do_search()

        if not points:
            raise Exception('Could not creat corridor from %s to %s' % (start, end))

        self.board.remove_entity(self.board[start].terrain)
        self.board.remove_entity(self.board[end].terrain)

        if points:
            for point in points:
                self.board.remove_entity(self.board[point].terrain)


        return points

    def flood_find(self, start, points=None, is_connected=None):
        """returns a set of points connected to the given point (including it),
        optionally using a provided is_connection function
        """
        if not points:
            points = self.region.empty_points()

        if not is_connected:
            is_connected = lambda point: self.board[point].terrain is None

        points = set(points)

        connected = set()
        processed = set()
        to_process = [start]

        while to_process:
            for point in to_process[:]:
                to_process.remove(point)
                if point not in processed:
                    processed.add(point)
                    if point in points and (point == start or is_connected(point)):
                        connected.add(point)
                        to_process.extend(geometry.adjacent(point))

        return connected

    def find_zones(self, points=None, is_connected = None):
        zones = []
        if not points:
            points = self.region.empty_points()

        processed = set()
        to_process = list(points)

        while to_process:
            point = to_process[0]
            zone = self.flood_find(point, points=points, is_connected=is_connected)
            for p in zone:
                to_process.remove(p)

            zones.append(zone)

        return zones

