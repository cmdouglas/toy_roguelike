import random

from rl.util import dice, tools, geometry
from rl.board.generator.painters import painter
from rl.board.generator import maparea
from rl.entities.obstacles import wall, smoothwall, door


class RoomClusterPainter(painter.Painter):
    def paint(self):
        num_rooms = dice.d(3, 2)

        border = self.get_border()
        points = set(self.area.get_all_points) - border

        valid_room_seeds = False
        rooms = []
        room_borders = set()
        while not valid_room_seeds:
            seeds = random.sample(points, num_rooms)
            room_borders = set()
            for seed in seeds:
                room_borders += set(tools.neighbors(seed))

            ok = True
            for seed in seeds:
                if seed in room_borders:
                    ok = False

            if ok:
                valid_room_seeds = True
                for seed in seeds:
                    rooms.append(geometry.Rectangle(seed, 1, 1))

    def grow_rectangle(self, rectangle, boundaries):
        pass






