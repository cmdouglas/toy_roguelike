##
# Still to do:
#
# 1.  Once the room shapes are generated, then find adjacency information and connect them to each other/the exits.
#     if there are orphans, then connect them to the main group by drawing corridors.  Use the room class with it's
#     door_candidates method for connection points.  We'll need to keep track of which walls are truly external
#     somehow.

import random

from rl.util import dice, geometry
from rl.util.bubble import BubbleField
from rl.board.generator.painters import painter
from rl.board.rooms.room import Room
from rl.entities.obstacles import wall, smoothwall, door


class RoomCluster:
    def __init__(self, rooms, painter):
        self.outsize_zones = []
        self.rooms = rooms
        self.disconnected_subclusters = []
        self.painter = painter

        self.find_outside_zones()
        self.find_adjacencies()
        self.find_disconnected_subclusters()

    def find_outside_zones(self):
        points = self.painter.area.get_all_points()
        def is_connected(point):
            for room in self.rooms:
                if point in room.all_points():
                    return False

            return True

        for connection in self.painter.area.connections:
            point = connection['point']
            zone = None
            for zone_ in self.outsize_zones:
                if point in zone_:
                    zone = zone_

            if not zone:
                zone = self.painter.flood_find(point, points, is_connected)
                self.outsize_zones.append(zone)

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

    def connect(self):
        # first connect the rooms within each subcluster
        for cluster in self.disconnected_subclusters:
            disconnected = cluster[:]
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

        # if there are more than one subcluster, connect them with a corridor

        # finally, connect each area connection to a room

class ClusterableRoom(Room):
    def __init__(self, shape):
        super().__init__(shape)
        self.adjacent = []
        self.connections = []

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

    def find_adjacency(self, other):
        adjacency = None
        for adjacency in self.adjacent:
            if adjacency['room'] == other:
                return adjacency

        my_door_candidates = set(self.door_candidates())
        other_door_candidates = set(other.door_candidates())

        adjacency_points = my_door_candidates.intersection(other_door_candidates)
        if (adjacency_points):
            adjacency = {
                'room': other,
                'points': adjacency_points
            }
            self.adjacent.append(adjacency)

        return adjacency


class RoomClusterPainter(painter.Painter):
    def paint(self):
        num_bubbles = dice.d(2, 3) + 1

        blocked = set(self.area.border())
        for connection in self.area.connections:
            point = connection['point']
            blocked.add(point)
            blocked.update(geometry.neighbors(point))

        field = BubbleField(self.area, blocked, num_bubbles)
        field.expand_bubbles()

        self.fill(wall.Wall)

        rooms = []

        for bubble in field.bubbles:
            rooms.append(ClusterableRoom(bubble.rect))

        ## test case for 2 disconnected subclusters
        #
        # for rect in [
        #     geometry.Rectangle((4, 4), 3, 3),
        #     geometry.Rectangle((8, 4), 3, 3),
        #
        #     geometry.Rectangle((4, 15), 3, 3),
        #     geometry.Rectangle((8, 15), 3, 3)
        # ]:
        #    rooms.append(ClusterableRoom(rect))

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
