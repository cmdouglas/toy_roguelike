import random

from rl.util import dice, tools, geometry
from rl.board.generator.painters import painter
from rl.board.generator import maparea
from rl.entities.obstacles import wall, smoothwall, door


class RoomClusterPainter(painter.Painter):
    def paint(self):
        num_rooms = dice.d(3, 2)
        pressure = 40

        border = set(self.get_border())
        points = set(self.area.get_all_points()) - border

        valid_room_seeds = False
        rooms = []
        room_borders = set()
        while not valid_room_seeds:
            seeds = random.sample(points, num_rooms)
            room_borders = set()
            for seed in seeds:
                room_borders = room_borders.union(set(tools.neighbors(seed)))

            ok = True
            for seed in seeds:
                if seed in room_borders:
                    ok = False

            if ok:
                valid_room_seeds = True
                for seed in seeds:
                    rooms.append(geometry.Rectangle(seed, 1, 1))

        changed = True
        while changed:
            changed = False
            for room in rooms:
                if len(room.points) >=pressure:
                    continue

                boundaries = set(self.get_border())
                for room_ in rooms:
                    if room_ is not room:
                        boundaries = boundaries.union(set(room_.border))

                changed = changed or self.grow_rectangle(room, boundaries)

            random.shuffle(rooms)

        self.fill(wall.Wall)
        for room in rooms:
            for point in room.points:
                self.board.remove_entity(self.board[point].obstacle)

            for point in room.border:
                self.board.remove_entity(self.board[point].obstacle)
                self.board.add_entity(wall.Wall(), point)


    def grow_rectangle(self, rectangle, boundaries):

        directions = [
            geometry.NORTH, geometry.SOUTH, geometry.EAST, geometry.WEST
        ]

        random.shuffle(directions)

        for direction in directions:
            if self.rectangle_can_grow(rectangle, direction, boundaries):
                rectangle.grow(direction)
                return True

        return False

    def rectangle_can_grow(self, rectangle, direction, boundaries):
        edge = rectangle.edge(direction)
        for point in edge:
            if point in boundaries:
                return False

        return True








