import random

from rl.util import geometry


class MapRegionConnectionException(Exception):
    pass


class MapRegion:
    def __init__(self, shape=None, board=None):
        self.shape = shape
        self.board = board
        self.adjacent = {}
        self.connections = {}

    @property
    def ul_pos(self):
        if isinstance(self.shape, geometry.Rectangle):
            return self.shape.ul
        else:
            raise NotImplementedError()

    def empty_points(self):
        return [point for point in self.shape.points
                if self.board[point].actor is None
                and self.board[point].terrain is None]

    def find_neighbors(self, regions):
        for region in regions:
            if region == self:
                continue

            if region in self.adjacent:
                continue

            self.find_adjacency(region)

    def connectible_neighbors(self):
        return [n for n in self.adjacent
                if len(self.connection_candidates(n)) > 0]

    def find_adjacency(self, region):
        adjacency = {}
        for point in self.shape.border & region.shape.outline:
            for neighbor in geometry.adjacent(point):
                if not neighbor in region.shape.points:
                    continue
                if not adjacency.get(point):
                    adjacency[point] = [neighbor]
                else:
                    adjacency[point].append(neighbor)

        if adjacency:
            self.adjacent[region] = adjacency

    def connect_to(self, region, points=None):
        if region not in self.adjacent:
            raise MapRegionConnectionException(
                'Cannot connect to {r1} to {r2} -- they are not adjacent.'
                    .format(r1=self, r2=region)
            )

        candidates = self.connection_candidates(region)
        if not candidates:
            raise MapRegionConnectionException(
                'Cannot connect to {r1} to {r2} -- no viable points for connection'
                    .format(r1=self, r2=region)
            )

        if points:
            mine, theirs = points
            if points not in candidates:
                raise MapRegionConnectionException(
                    'Cannot connect to {r1} to {r2} at {p1, p2}'
                        .format(r1=self, r2=region, p1=mine, p2=theirs)
                )

        else:
            mine, theirs = random.choice(candidates)

        self.connections[mine] = (region, theirs)
        region.connections[theirs] = (self, mine)

    def connection_candidates(self, region):
        adjacency = self.adjacent[region]
        points = []
        for c1 in [p for p in adjacency.keys() if self.is_viable_connection_point(p)]:
            for c2 in [p for p in adjacency[c1] if region.is_viable_connection_point(p)]:
                points.append((c1, c2))
        return points

    def is_viable_connection_point(self, point):
        # points not on the border are right out
        if not point in self.shape.border:
            return False

        north, east, south, west = geometry.adjacent(point)

        # points on corners are undesirable
        if not ((east in self.shape.border and west in self.shape.border) or
                (north in self.shape.border and south in self.shape.border)):
            return False

        # we also don't want points next to other connections
        for neighbor in north, east, south, west:
            if neighbor in self.connections:
                return False

        return True

    def __getstate__(self):
        state = dict(
            _save_id=id(self),
            shape=self.shape,
        )
        adjacent = {}
        for neighbor, adjacencies in self.adjacent.items():
            adjacent[id(neighbor)] = adjacencies

        state['adjacent'] = adjacent

        connections = {}
        for point, connection in self.connections.items():
            other_region, other_point = connection
            connections[point] = (id(other_region), other_point)

        state['connections'] = connections

        return state

    def __setstate__(self, state):
        self.shape = state['shape']

        self.loaded_data = state
