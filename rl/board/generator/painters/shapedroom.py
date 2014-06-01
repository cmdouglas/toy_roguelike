import random

from rl.objects.obstacles import smoothwall, wall, door
from rl.util import shape
from rl.util import dice
from rl.board.rooms import room as room_mod
from rl.board.generator.painters import painter
from rl.board.generator import maparea
from rl.objects.items import potion


class ShapedRoomPainter(painter.Painter):
    def get_bounding_box(self):
        area_left, area_top = self.area.ul_pos

        area_left += 2
        area_top += 2
                
        width = self.area.width - 4
        height = self.area.height - 4
        
        rectangle_width = random.randrange(int(width / 2), width)
        rectangle_height = random.randrange(int(height / 2), height)
        
        horizontal_offset = 0
        vertical_offset = 0
        
        if width - rectangle_width > 1:
            horizontal_offset = random.randrange(width - rectangle_width)
        
        if height - rectangle_height > 1:
            vertical_offset = random.randrange(height - rectangle_height)
        
        rectangle_center = (
            area_left + horizontal_offset + rectangle_width / 2,
            area_top + vertical_offset + rectangle_height / 2)
            
        return (rectangle_center, rectangle_width, rectangle_height)
        
    def area_meets_requirements(self):
        return self.area.width > 8 and self.area.height > 8

class RectangularRoomPainter(ShapedRoomPainter):
    def paint(self):
        self.fill(wall.Wall)
        center, width, height = self.get_bounding_box()
        
        rectangle = shape.Rectangle(center, width, height)
        room = room_mod.Room(rectangle)

        # place 1d3 doors
        doorsteps = []
        for _ in range(dice.d(1, 3)):
            door_pos = random.choice(room.door_candidates())
            room.place_door(door_pos)
            doorsteps.append(room.doorstep(door_pos))

        #draw room
        for pos in room.interior:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            
        for pos in room.walls:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            self.board.add_object(smoothwall.SmoothWall(), pos)

        for pos in room.doors:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            self.board.add_object(door.Door(), pos)

        # draw corridors
        border_points = [c['point'] for c in self.area.connections]
        blocked = set(room.all_points())

        connected_doorsteps = []

        for p in border_points:
            self.board.remove_object(self.board[p].objects['obstacle'])
            doorstep = random.choice(doorsteps)
            connected_doorsteps.append(doorstep)
            self.smart_draw_corridor(p, doorstep, blocked)

        for p in doorsteps:
            if p not in connected_doorsteps:
                self.board.remove_object(self.board[p].objects['obstacle'])
                border_point = random.choice(border_points)
                self.smart_draw_corridor(p, border_point, blocked)
            
        self.board[center].add_item(potion.HealingPotion())
            
class CircularRoomPainter(ShapedRoomPainter):
    def paint(self):
        self.fill(wall.Wall)
        center, width, height = self.get_bounding_box()

        circle = shape.Circle(center, min(width, height)/2)
        room = room_mod.Room(circle)

        # place 1d3 doors
        doorsteps = []
        for _ in range(dice.d(1, 3)):
            door_pos = random.choice(room.door_candidates())
            room.place_door(door_pos)
            doorsteps.append(room.doorstep(door_pos))

        #draw room
        for pos in room.interior:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])

        for pos in room.walls:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            self.board.add_object(smoothwall.SmoothWall(), pos)

        for pos in room.doors:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            self.board.add_object(door.Door(), pos)

        # draw corridors
        border_points = [c['point'] for c in self.area.connections]
        blocked = set(room.all_points())

        connected_doorsteps = []

        for p in border_points:
            self.board.remove_object(self.board[p].objects['obstacle'])
            doorstep = random.choice(doorsteps)
            connected_doorsteps.append(doorstep)
            self.smart_draw_corridor(p, doorstep, blocked)

        for p in doorsteps:
            if p not in connected_doorsteps:
                self.board.remove_object(self.board[p].objects['obstacle'])
                border_point = random.choice(border_points)
                self.smart_draw_corridor(p, border_point, blocked)
            
        self.board[center].add_item(potion.HealingPotion())
            
            
class EllipticalRoomPainter(ShapedRoomPainter):

    def paint(self):
        self.fill(wall.Wall)
        center, width, height = self.get_bounding_box()

        ellipse = shape.Ellipse(center, width/2, height/2)
        room = room_mod.Room(ellipse)

        # place 1d3 doors
        doorsteps = []
        for _ in range(dice.d(1, 3)):
            door_pos = random.choice(room.door_candidates())
            room.place_door(door_pos)
            doorsteps.append(room.doorstep(door_pos))

        #draw room
        for pos in room.interior:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])

        for pos in room.walls:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            self.board.add_object(smoothwall.SmoothWall(), pos)

        for pos in room.doors:
            tile = self.board[pos]
            self.board.remove_object(tile.objects['obstacle'])
            self.board.add_object(door.Door(), pos)

        # draw corridors
        border_points = [c['point'] for c in self.area.connections]
        blocked = set(room.all_points())

        connected_doorsteps = []

        for p in border_points:
            self.board.remove_object(self.board[p].objects['obstacle'])
            doorstep = random.choice(doorsteps)
            connected_doorsteps.append(doorstep)
            self.smart_draw_corridor(p, doorstep, blocked)

        for p in doorsteps:
            if p not in connected_doorsteps:
                self.board.remove_object(self.board[p].objects['obstacle'])
                border_point = random.choice(border_points)
                self.smart_draw_corridor(p, border_point, blocked)

        self.board[center].add_item(potion.HealingPotion())
        

