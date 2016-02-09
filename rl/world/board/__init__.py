import logging
import random

from rl.world.board.tile import Tile, EntityPlacementException
from rl.world.entities.actors.creatures.player import Player

#from rl.save import rl_types

logger = logging.getLogger('rl')



class Board:
    def __init__(self, width, height, world=None):
        self.width = width
        self.height = height
        self.world = world
        self.actors = []

        self.rows = [
            [Tile(self, (x, y)) for x in range(self.width)]
            for y in range(self.height)
        ]

        self.regions = []
        self.visible = set()
        self.remembered = {}

    def __getitem__(self, pos):
        x, y = pos
        return self.rows[int(y)][int(x)]

    def position_is_valid(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    @property
    def tiles(self):
        for row in self.rows:
            for tile in row:
                yield tile

    def spawn_player(self):
        player = Player()
        region = random.choice(self.regions)
        pos = random.choice(region.empty_points())
        self[pos].creature = player

        self.update_fov(player)

        return player

    def find_player(self):
        for actor in self.actors:
            if isinstance(actor, Player):
                return actor

    def update_fov(self, player):

        visible_points = self.get_visible_points(
            player.tile.pos, player.sight_radius
        )
        self.visible = set([point for point in visible_points if self.position_is_valid(point)])

        for point in visible_points:
            if self.position_is_valid(point):
                tile = self[point]

                if tile.pos not in self.remembered.keys():
                    tile.on_first_seen()

                self.remember_tile(tile)

    def region_containing_point(self, point):
        for region in self.regions:
            if point in region.shape.points:
                return region

        return None

    def nearby_reachable_points(self, pos, distance):
        points = []

        def _add_empty_neighbors(p, d):
            candidates = self[p].neighbors()
            for candidate in candidates:
                if (not candidate.blocks_movement() and
                   candidate.pos not in points):

                    points.append(candidate.pos)
                    if d > 0:
                        _add_empty_neighbors(candidate.pos, d-1)
        _add_empty_neighbors(pos, distance)

        return points

    def get_visible_points(self, pos, radius):
        directions = [
            (1,  0,  0,  1),
            (0,  1,  1,  0),
            (0, -1,  1,  0),
            (-1, 0,  0,  1),
            (-1, 0,  0, -1),
            (0, -1, -1,  0),
            (0,  1, -1,  0),
            (1,  0,  0, -1)
        ]

        visible = []

        # you can see the tile you're standing on
        visible.append(pos)

        def is_blocked(pos):
            return not self.position_is_valid(pos) or self[pos].blocks_vision()

        def cast_light(center, row, start, end, radius, mult, id=0):
            "Recursive lightcasting function"
            cx, cy = center
            xx, xy, yx, yy = mult

            if start < end:
                return
            radius_squared = radius*radius
            for j in range(row, radius+1):
                dx, dy = -j-1, -j
                blocked = False
                new_start = None
                while dx <= 0:
                    dx += 1
                    # Translate the dx, dy coordinates into map coordinates:
                    x, y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                    # l_slope and r_slope store the slopes of the left and
                    # right extremities of the square we're considering:
                    l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
                    if start < r_slope:
                        continue
                    elif end > l_slope:
                        break
                    else:
                        # Our light beam is touching this square; light it:
                        if dx*dx + dy*dy < radius_squared:
                            visible.append((x, y))
                        if blocked:
                            # we're scanning a row of blocked squares:
                            if is_blocked((x, y)):
                                new_start = r_slope
                                continue
                            else:
                                blocked = False
                                start = new_start
                        else:
                            if is_blocked((x, y)) and j < radius:
                                # This is a blocking square, start a child scan
                                blocked = True
                                cast_light(center, j+1, start, l_slope,
                                           radius, mult, id+1)
                                new_start = r_slope
                # Row is scanned; do next row unless last square was blocked:
                if blocked:
                    break

        for d in directions:
            cast_light(pos, 1, 1.0, 0.0, radius, d)

        return visible

    def __getstate__(self):
        state = dict(
            width=self.width,
            height=self.height,
            regions=self.regions,
            tiles={tile.pos: tile for tile in self.tiles}
        )

        return state

    def __setstate__(self, state):
        self.__init__(state['width'], state['height'])
        for pos, tile in state['tiles'].items():
            x, y = pos
            self.rows[int(y)][int(x)] = tile
            tile.board = self
            tile.pos = pos
            if tile.creature:
                self.actors.append(tile.actor)

        self.regions = state['regions']

        # reconnect the regions
        regions_by_id = {region.loaded_data['_save_id']: region for region in state['regions']}
        for region in self.regions:
            region.board = self
            adjacent = {}
            for neighbor_id, adjacency in region.loaded_data['adjacent'].items():
                adjacent[regions_by_id[neighbor_id]] = adjacency

            region.adjacent = adjacent

            connections = {}
            for point, connection in region.loaded_data['connections'].items():
                other_region_id, other_point = connection
                connections[point] = (regions_by_id[other_region_id], other_point)

            region.connections = connections

        from rl.world.ai.basic import BasicAI
        from rl.world.ai.strategies.aggressive import AggressiveStrategy
        actors_by_id = {actor._save_id: actor for actor in self.actors}

        for actor in self.actors:
            if isinstance(actor.intelligence, BasicAI) and isinstance(actor.intelligence.strategy, AggressiveStrategy):
                actor.intelligence.strategy.target = actors_by_id.get(actor.intelligence.strategy.target)
