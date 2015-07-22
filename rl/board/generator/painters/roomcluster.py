##
# Still to do:
# 1.  spin the bubble-field code off into its own module.  I'm not sure if I'll use it for anything else, but it's
#     cluttering up this file and making it difficult to read.
#     this entails: making the bubble field unaware of the area, instead it should just have some points it can play
#     with and know which of those are out of bounds.
#
# 2.  Once the room shapes are generated, then find adjacency information and connect them to each other/the exits.
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
        self.painter = painter

        self.find_outside_zones()

    def find_outside_zones(self):
        pass



class ClusterableRoom(Room):
    def __init__(self, shape):
        super().__init__(shape)
        self.adjacent = []
        self.connections = []

    def connect_with_door(self, other, point):
        assert point in self.door_candidates()
        assert point in other.door_candidates()
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
            for point in bubble.rect.points:
                self.board.remove_entity(self.board[point].obstacle)

            for point in bubble.rect.border:
                self.board.remove_entity(self.board[point].obstacle)
                self.board.add_entity(smoothwall.SmoothWall(), point)

        cluster = RoomCluster(rooms, self)
