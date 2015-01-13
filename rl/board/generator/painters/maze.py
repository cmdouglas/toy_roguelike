import random
import math

from rl.entities.obstacles.wall import Wall
from rl.util import dice, tools
from rl.board.generator.painters import painter
from rl.board.generator import maparea

class MazeCell:
    def __init__(self, point, board, area):
        self.point = point
        self.board = board
        self.area = area
        self.walls = self.border()
        self.visited = False

        self.board.remove_entity(self.board[self.point].obstacle)

    def border(self):
        b = set()

        neighbors = tools.adjacent(self.point)
        for neighbor in neighbors:
            if self.area.contains_point(neighbor):
                b.add(neighbor)

        return b

    def remove_wall(self, point):
        if point in self.walls:
            self.board.remove_entity(self.board[point].obstacle)
            self.walls.remove(point)

class MazeCellGrid:
    def __init__(self, board, area):
        self.board = board
        self.area = area

        self.rows = []
        ul_x, ul_y = self.area.ul_pos
        x, y = ul_x + 1, ul_y + 1

        while y < ul_y + self.area.height - 1:
            row = []
            x = ul_x + 1
            while x < ul_x + self.area.width -1:
                row.append(MazeCell((x, y), self.board, self.area))
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
        return [(neighbor, self.get_cell(neighbor)) for neighbor in neighbors if self.get_cell(neighbor).visited == False]

    def get_cell(self, pos):
        x, y = pos
        return self.rows[y][x]

    def random_cell(self):
        y, row = random.choice(list(enumerate(self.rows)))
        x, cell = random.choice(list(enumerate(row)))

        return ((x, y), cell)


class MazePainter(painter.Painter):
    def paint(self):
        self.fill(Wall)


        cellgrid = MazeCellGrid(self.board, self.area)
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


        for connection in self.area.connections:
            x, y = connection['point']
            points = [(x, y)]

            if connection['side'] == maparea.TOP:
                points.append((x, y+1))
            elif connection['side'] == maparea.BOTTOM:
                points.append((x, y-1))
            elif connection['side'] == maparea.LEFT:
                points.append((x+1, y))
            elif connection['side'] == maparea.RIGHT:
                points.append((x-1, y))

            for point in points:
                self.board.remove_entity(self.board[point].obstacle)

        empty_points = self.area.get_empty_points()

        to_fill = random.randrange(int(math.sqrt(len(empty_points))), int(len(empty_points) / 2))

        def is_dead_end(point):
            adjacent = tools.adjacent(point)
            walls = 0
            for adjacent_point in adjacent:
                if self.area.contains_point(adjacent_point) and self.board[adjacent_point].obstacle:
                    walls += 1

            return walls == 3

        def free_space_adjacent_dead_end(point):
            adjacent = tools.adjacent(point)
            for adjacent_point in adjacent:
                if self.area.contains_point(adjacent_point) and not self.board[adjacent_point].obstacle:
                    return adjacent_point

        dead_ends = [point for point in self.area.get_empty_points() if is_dead_end(point)]
        for _ in range(to_fill):
            if not dead_ends:
                break
            dead_end = random.choice(dead_ends)
            dead_ends.remove(dead_end)
            self.board.add_entity(Wall(), dead_end)


            new_dead_end = free_space_adjacent_dead_end(dead_end)

            if new_dead_end and is_dead_end(new_dead_end):
                dead_ends.append(new_dead_end)






