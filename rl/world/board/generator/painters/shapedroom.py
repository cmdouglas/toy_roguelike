import random

from rl.world.entities.obstacles import smoothwall, wall, door
from rl.util import geometry
from rl.util import dice
from rl.world.board.rooms import Room
from rl.world.board.generator.painters import Painter


class ShapedRoomPainter(Painter):
    def get_bounding_box(self):
        region_left, region_top = self.region.shape.ul

        region_left += 3
        region_top += 3
                
        width = self.region.shape.width - 6
        height = self.region.shape.height - 6
        
        rectangle_width = random.randrange(int(width / 2), width)
        rectangle_height = random.randrange(int(height / 2), height)
        
        horizontal_offset = 0
        vertical_offset = 0
        
        if width - rectangle_width > 1:
            horizontal_offset = random.randrange(width - rectangle_width)
        
        if height - rectangle_height > 1:
            vertical_offset = random.randrange(height - rectangle_height)
        
        rectangle_center = (
            region_left + horizontal_offset + rectangle_width / 2,
            region_top + vertical_offset + rectangle_height / 2)
            
        return (rectangle_center, rectangle_width, rectangle_height)

    @classmethod
    def region_meets_requirements(cls, region):
        #TODO: make this check unnecessary
        if not isinstance(region.shape, geometry.Rectangle):
            return False

        return region.shape.width >= 10 and region.shape.height >= 10


class RectangularRoomPainter(ShapedRoomPainter):
    def paint(self):
        self.fill(wall.Wall)
        center, width, height = self.get_bounding_box()
        
        rectangle = geometry.Rectangle(center, width, height)
        room = Room(rectangle)

        # place 1d3 doors
        doorsteps = []
        for _ in range(dice.d(1, 3)):
            door_pos = random.choice(room.door_candidates())
            room.place_door(door_pos)
            doorsteps.append(room.doorstep(door_pos))

        #draw room
        for pos in room.interior:
            tile = self.board[pos]
            self.board.remove_entity(tile.obstacle)
            
        for pos in room.walls:
            tile = self.board[pos]
            self.board.remove_entity(tile.obstacle)
            self.board.add_entity(smoothwall.SmoothWall(), pos)

        for pos in room.doors:
            tile = self.board[pos]
            self.board.remove_entity(tile.obstacle)
            self.board.add_entity(door.Door(), pos)

        # draw corridors
        connections = list(self.region.connections.keys())
        blocked = set(room.all_points()).union(set(self.region.shape.border))
        blocked -= set(connections)

        connected_doorsteps = []

        for p in connections:
            self.board.remove_entity(self.board[p].obstacle)
            doorstep = random.choice(doorsteps)
            connected_doorsteps.append(doorstep)
            self.smart_draw_corridor(p, doorstep, blocked)

        for p in doorsteps:
            if p not in connected_doorsteps:
                self.board.remove_entity(self.board[p].obstacle)
                border_point = random.choice(connections)
                self.smart_draw_corridor(p, border_point, blocked)


class CircularRoomPainter(ShapedRoomPainter):
    def paint(self):
        self.fill(wall.Wall)
        center, width, height = self.get_bounding_box()

        circle = geometry.Circle(center, min(width, height)/2)
        room = Room(circle)

        # place 1d3 doors
        doorsteps = []
        for _ in range(dice.d(1, 3)):
            door_pos = random.choice(room.door_candidates())
            room.place_door(door_pos)
            doorsteps.append(room.doorstep(door_pos))

        #draw room
        for pos in room.interior:
            tile = self.board[pos]
            self.board.remove_entity(tile.obstacle)

        for pos in room.walls:
            tile = self.board[pos]
            self.board.remove_entity(tile.obstacle)
            self.board.add_entity(smoothwall.SmoothWall(), pos)

        for pos in room.doors:
            tile = self.board[pos]
            self.board.remove_entity(tile.obstacle)
            self.board.add_entity(door.Door(), pos)

        # draw corridors
        connections = list(self.region.connections.keys())
        blocked = set(room.all_points()).union(set(self.region.shape.border))
        blocked -= set(connections)

        connected_doorsteps = []

        for p in connections:
            self.board.remove_entity(self.board[p].obstacle)
            doorstep = random.choice(doorsteps)
            connected_doorsteps.append(doorstep)
            self.smart_draw_corridor(p, doorstep, blocked)

        for p in doorsteps:
            if p not in connected_doorsteps:
                self.board.remove_entity(self.board[p].obstacle)
                border_point = random.choice(connections)
                self.smart_draw_corridor(p, border_point, blocked)

            
class EllipticalRoomPainter(ShapedRoomPainter):

    def paint(self):
        self.fill(wall.Wall)
        center, width, height = self.get_bounding_box()

        ellipse = geometry.Ellipse(center, width/2, height/2)
        room = Room(ellipse)

        # place 1d3 doors
        doorsteps = []
        for _ in range(dice.d(1, 3)):
            door_pos = random.choice(room.door_candidates())
            room.place_door(door_pos)
            doorsteps.append(room.doorstep(door_pos))

        #draw room
        for pos in room.interior:
            tile = self.board[pos]
            self.board.remove_entity(tile.obstacle)

        for pos in room.walls:
            tile = self.board[pos]
            self.board.remove_entity(tile.obstacle)
            self.board.add_entity(smoothwall.SmoothWall(), pos)

        for pos in room.doors:
            tile = self.board[pos]
            self.board.remove_entity(tile.obstacle)
            self.board.add_entity(door.Door(), pos)

        # draw corridors
        connections = list(self.region.connections.keys())
        blocked = set(room.all_points()).union(set(self.region.shape.border))
        blocked -= set(connections)

        connected_doorsteps = []

        for p in connections:
            self.board.remove_entity(self.board[p].obstacle)
            doorstep = random.choice(doorsteps)
            connected_doorsteps.append(doorstep)
            self.smart_draw_corridor(p, doorstep, blocked)

        for p in doorsteps:
            if p not in connected_doorsteps:
                self.board.remove_entity(self.board[p].obstacle)
                border_point = random.choice(connections)
                self.smart_draw_corridor(p, border_point, blocked)


