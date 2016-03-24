import random

from rl.world.entities.terrain import wall
from rl.util import dice, geometry
from rl.world.board.generator.painters import Painter


class TunnelPainter(Painter):
    @classmethod
    def region_meets_requirements(cls, region):
        # no dead end tunnels
        return len(region.connections) >= 2

class SnakeyTunnelPainter(TunnelPainter):
    def paint(self):
        self.terrain_fill(wall.Wall)
        border = self.region.shape.border
        connections = list(self.region.connections.keys())[:]
        costs = {}
        base_cost = 1000
        for point in self.region.shape.points:
            costs[point] = base_cost

        for point in border:
            costs[point] = 10*base_cost

        random.shuffle(connections)

        path_endpoints = connections[0:2]
        extra_connections = connections[2:]

        inflection_candidates = list(set(self.region.shape.points) - set(self.region.shape.border))

        inflection_points = []
        for i in range(dice.d(2, 2)):
            p = random.choice(inflection_candidates)
            inflection_points.append(p)
            inflection_candidates.remove(p)

        path_start, path_end = path_endpoints
        path = [path_start] + inflection_points + [path_end]

        for point in path:
            costs[point] = 40*base_cost
            for n in geometry.neighbors(point):
                costs[n] = 10*base_cost

        segments = []
        
        for i, point in enumerate(path[:-1]):
            segments.append((point, path[i+1]))

        # dig out the path
        for segment in segments:
            start, end = segment
            dug = self.smart_draw_corridor(start, end, costs=costs)
            for p in dug:
                costs[p] = 10*base_cost
                for p in geometry.neighbors(p):
                    if p not in dug:
                        costs[p] = 10*base_cost

        #connect any extra access points to the path
        for start in extra_connections:
            end = random.choice(inflection_points)
            dug = self.smart_draw_corridor(start, end, costs=costs)
            for p in dug:
                # try and keep adacent tunnels from being dug
                costs[p] = 10*base_cost
                for p in geometry.neighbors(p):
                    if p not in dug:
                        costs[p] = 10*base_cost
