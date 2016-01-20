import random

from rl.util import dice, geometry, tools
from rl.util.bubble import BubbleField
from rl.world.board.generator.painters import Painter
from rl.world.board.rooms import Room
from rl.world.entities.terrain import wall, smoothwall, door


class RoomCluster:
    def __init__(self, rooms, painter):
        self.outside_zones = []
        self.rooms = rooms
        self.disconnected_subclusters = []
        self.painter = painter

        self.find_outside_zones()
        self.find_adjacencies()
        self.find_disconnected_subclusters()
        self.find_potential_outside_connections()

    def all_points(self):
        points = set()
        for room in self.rooms:
            points.update(room.all_points())

        return points

    def find_outside_zones(self):
        points = self.painter.region.shape.points

        def is_connected(p):
            for room in self.rooms:
                if p in room.all_points():
                    return False

            return True

        for point in self.painter.region.connections.keys():
            zone = None
            for zone_ in self.outside_zones:
                if point in zone_:
                    zone = zone_

            if not zone:
                zone = self.painter.flood_find(point, points, is_connected)
                self.outside_zones.append(zone)

    def find_potential_outside_connections(self):
        for zone in self.outside_zones:
            for room in self.rooms:
                room.find_outside_connections(zone)

    def find_adjacencies(self):
        for room1 in self.rooms:
            for room2 in self.rooms:
                if room1 != room2:
                    room1.find_adjacency(room2)

    def find_reachable_rooms(self, room):
        reachable_rooms = [room]

        def _recursive_room_search(room):
            found = False
            for adjacency in room.adjacent:
                reachable_room = adjacency['room']
                if reachable_room not in reachable_rooms:
                    reachable_rooms.append(reachable_room)
                    found = True

                if found:
                    for adjacency in room.adjacent:
                        reachable_room = adjacency['room']
                        _recursive_room_search(reachable_room)

        _recursive_room_search(room)
        return reachable_rooms

    def find_disconnected_subclusters(self):
        for room in self.rooms:
            cluster = None

            for cluster_ in self.disconnected_subclusters:
                if room in cluster_:
                    cluster = cluster_

            if not cluster:
                cluster = self.find_reachable_rooms(room)
                self.disconnected_subclusters.append(cluster)

        return self.disconnected_subclusters

    def connect_within_subcluster(self, subcluster):
        disconnected = subcluster[:]
        room = random.choice(disconnected)

        while disconnected:
            # if the room has no adjacencies, don't try to connect with anything
            if not room.adjacent:
                break

            adjacent = [adj['room'] for adj in room.adjacent]
            disconnected_adjacent = [adj['room'] for adj in room.adjacent if adj['room'] in disconnected]

            if disconnected_adjacent:
                room2 = random.choice(disconnected_adjacent)

            elif room in disconnected:
                room2 = random.choice(room.adjacent)

            else:
                room = random.choice(adjacent)
                continue

            room.connect_with_door(room2)
            if room in disconnected:
                disconnected.remove(room)

            if room2 in disconnected:
                disconnected.remove(room2)

            if dice.one_chance_in(6):
                room3 = random.choice(adjacent)
                room.connect_with_door(room3)
                if room3 in disconnected:
                    disconnected.remove(room3)

            room = room2

    def connect_subclusters(self, subcluster1, subcluster2):
        random.shuffle(subcluster1)
        random.shuffle(subcluster2)

        for room1 in subcluster1:
            for room2 in subcluster2:
                for zone in self.outside_zones:
                    r1_candidates = set()
                    for zone_, connections in room1.potential_outside_connections:
                        if zone_ == zone:
                            r1_candidates = connections.intersection(set(room1.door_candidates()))

                    r2_candidates = set()
                    for zone_, connections in room2.potential_outside_connections:
                        if zone_ == zone:
                            r2_candidates = connections.intersection(set(room2.door_candidates()))

                    if r1_candidates and r2_candidates:
                        p1 = random.choice(list(r1_candidates))
                        p2 = random.choice(list(r2_candidates))

                        room1.place_door(p1)
                        room2.place_door(p2)

                        self.painter.smart_draw_corridor(
                            room1.doorstep(p1), room2.doorstep(p2), blocked=self.all_points()
                        )
                        return

    def connect_to_access_points(self):
        for access_point in self.painter.region.connections.keys():
            path_found = False
            for zone in self.outside_zones:
                if access_point in zone:
                    random.shuffle(self.rooms)
                    for room in self.rooms:
                        for zone_, connections in room.potential_outside_connections:
                            candidates = set()
                            if zone == zone_:
                                candidates = connections.intersection(set(room.door_candidates()))

                            if candidates:
                                p = random.choice(list(candidates))
                                room.place_door(p)

                                self.painter.smart_draw_corridor(
                                    access_point, room.doorstep(p), blocked=self.all_points()
                                )
                                path_found = True
                        if path_found:
                            break

    def connect(self):
        # first connect the rooms within each subcluster
        for subcluster in self.disconnected_subclusters:
            self.connect_within_subcluster(subcluster)

        # if there are more than one subcluster, connect them with a corridor
        if len(self.disconnected_subclusters) >= 2:
            for cluster1, cluster2 in tools.pairwise(self.disconnected_subclusters):
                self.connect_subclusters(cluster1, cluster2)

        # finally, connect each region connection to a room
        self.connect_to_access_points()


class ClusterableRoom(Room):
    def __init__(self, shape):
        super().__init__(shape)
        self.adjacent = []
        self.connections = []
        self.potential_outside_connections = []

    def connect_with_door(self, other):
        adjacency = self.find_adjacency(other)

        points = adjacency['points']
        points = points.intersection(set(self.door_candidates()))
        points = points.intersection(set(other.door_candidates()))

        if not points:
            return

        point = random.choice(list(points))

        self.place_door(point)
        other.place_door(point)

        self.connections.append({
            'room': other,
            'point': point
        })

        other.connections.append({
            'room': self,
            'point': point
        })

    def find_outside_connections(self, outside_zone):
        connection_set = set()
        for point in self.door_candidates():
            for n in geometry.adjacent(point):
                if n in outside_zone:
                    connection_set.add(point)
        if connection_set:
            self.potential_outside_connections.append((outside_zone, connection_set))

    def find_adjacency(self, other):
        adjacency = None
        for adjacency in self.adjacent:
            if adjacency['room'] == other:
                return adjacency

        my_door_candidates = set(self.door_candidates())
        other_door_candidates = set(other.door_candidates())

        adjacency_points = my_door_candidates.intersection(other_door_candidates)
        if adjacency_points:
            adjacency = {
                'room': other,
                'points': adjacency_points
            }
            self.adjacent.append(adjacency)

        return adjacency


class RoomClusterPainter(Painter):
    def paint(self):
        num_bubbles = dice.d(2, 3) + 1

        blocked = set(self.region.shape.border)
        for point in self.region.connections.keys():
            blocked.add(point)
            blocked.update(geometry.neighbors(point))

        field = BubbleField(self.region, blocked, num_bubbles)
        field.expand_bubbles()

        self.fill(wall.Wall)
        for access_point in self.region.connections.keys():
            self.board.remove_entity(self.board[access_point].obstacle)

        rooms = []

        for bubble in field.bubbles:
            rooms.append(ClusterableRoom(bubble.rect))

        cluster = RoomCluster(rooms, self)
        cluster.connect()

        for room in rooms:
            for point in room.interior:
                self.board.remove_entity(self.board[point].obstacle)

            for point in room.walls:
                self.board.remove_entity(self.board[point].obstacle)
                self.board.add_entity(smoothwall.SmoothWall(), point)

            for point in room.doors:
                self.board.remove_entity(self.board[point].obstacle)
                self.board.add_entity(door.Door(), point)
