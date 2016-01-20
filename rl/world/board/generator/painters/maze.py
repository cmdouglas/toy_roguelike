
import random
import math

from rl.world.entities.obstacles.wall import Wall
from rl.util import geometry
from rl.world.board.generator.painters import Painter


class MazeCell:
    def __init__(self, point, board, region):
        self.point = point
        self.board = board
        self.region = region
        self.walls = self.border()
        self.visited = False

        self.board.remove_entity(self.board[self.point].obstacle)

    def border(self):
        b = set()

        neighbors = geometry.adjacent(self.point)
        for neighbor in neighbors:
            if neighbor in self.region.shape.points:
                b.add(neighbor)

        return b

    def remove_wall(self, point):
        if point in self.walls:
            self.board.remove_entity(self.board[point].obstacle)
            self.walls.remove(point)


class MazeCellGrid:
    def __init__(self, board, region):
        self.board = board
        self.region = region

        self.rows = []
        ul_x, ul_y = self.region.shape.ul
        x, y = ul_x + 1, ul_y + 1

        while y < ul_y + self.region.shape.height - 1:
            row = []
            x = ul_x + 1
            while x < ul_x + self.region.shape.width - 1:
                row.append(MazeCell((x, y), self.board, self.region))
                x += 2
            self.rows.append(row)
            y += 2

    def neighbors(self, cell_pos):
        x, y = cell_pos
        r = []

        for pos in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            nx, ny = pos
            if 0 <= ny < len(self.rows):
                if 0 <= nx < len(self.rows[0]):
                    r.append((nx, ny))

        return r

    def unvisited_neighbors(self, pos):
        neighbors = self.neighbors(pos)
        return [
            (neighbor, self.get_cell(neighbor))
            for neighbor in neighbors
            if self.get_cell(neighbor).visited is False
        ]

    def get_cell(self, pos):
        x, y = pos
        return self.rows[y][x]

    def random_cell(self):
        y, row = random.choice(list(enumerate(self.rows)))
        x, cell = random.choice(list(enumerate(row)))

        return ((x, y), cell)


class MazePainter(Painter):
    @classmethod
    def region_meets_requirements(cls, region):
        #TODO allow for non-rectangular regions
        return isinstance(region.shape, geometry.Rectangle)

    def paint(self):
        self.fill(Wall)

        cellgrid = MazeCellGrid(self.board, self.region)
        pos, start = cellgrid.random_cell()
        stack = [(pos, start)]

        while stack:
            pos, cell = stack[len(stack) - 1]
            cell.visited = True
            unvisited_neighbors = cellgrid.unvisited_neighbors(pos)
            if unvisited_neighbors:
                pos, neighbor = random.choice(unvisited_neighbors)
                walls = cell.border().intersection(neighbor.border())
                for wall in walls:
                    cell.remove_wall(wall)
                    neighbor.remove_wall(wall)

                stack.append((pos, neighbor))

            else:
                stack.pop()

        for connection in self.region.connections:
            nearest = geometry.sort_by_distance(self.region.empty_points(), connection)[0]
            self.smart_draw_corridor(nearest, connection)

        empty_points = self.region.empty_points()

        to_fill = random.randrange(
            int(math.sqrt(len(empty_points))), int(len(empty_points) / 2)
        )
        
        # TODO: do something interesting with dead ends -- there needs to be a good reason to explore!
        # maybe choose one of the following (with appropriate weights):
        #   place an item or monster in the dead end
        #   connect the dead end to a neighbor, creating a loop
        #   fill it in
        #   do nothing