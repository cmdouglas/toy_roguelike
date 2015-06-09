from rl.util import geometry

class Room(object):
    walls = []
    interior = []
    doors = []

    def __init__(self, shape):
        self.interior = shape.points
        self.walls = shape.border

    def place_door(self, pos):
        self.walls.remove(pos)
        self.doors.append(pos)

    def door_allowed(self, pos):
        if not pos in self.walls:
            return False

        n, e, s, w = geometry.adjacent(pos)

        return (n in self.walls and s in self.walls) or (e in self.walls and w in self.walls)

    def door_candidates(self):
        return [point for point in self.walls if self.door_allowed(point)]

    def all_points(self):
        return self.walls + self.interior + self.doors

    def doorstep(self, position):
        """returns the position immediately outside the room, and next to the supplied position"""
        for p in geometry.adjacent(position):
            if p in self.interior:
                continue

            if p in self.walls:
                continue

            if p in self.doors:
                continue

            return p

        return None