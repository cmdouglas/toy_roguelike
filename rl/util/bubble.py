"""Shaped bubble field implementation -- allows for creating a field
and placing (rectangular) bubbles in it and expanding them.

currently used for creating clusters of rooms
"""

import random
from rl.util import geometry


class BubbleField:
    target_areas = [4, 6, 6, 10, 10, 12, 20, 20, 30, 30, 40]
    target_ratios = [1/2, 2/3, 2/3, 3/4, 3/4, 1]

    def __init__(self, region, blocked, num_bubbles):
        self.num_bubbles = num_bubbles
        self.region = region
        self.blocked = blocked
        self.bubbles = []
        self.create_bubbles()

    def expand_bubbles(self):
        continue_expanding = True
        while continue_expanding:
            continue_expanding = False
            for bubble in self.bubbles:
                something_expanded = bubble.expand()
                continue_expanding = continue_expanding or something_expanded

    def create_bubbles(self):
        ul_x, ul_y = self.region.ul_pos
        center = (int(ul_x + self.region.width/2), int(ul_y + self.region.height/2))
        cx, cy = center

        points = set()
        for x in range(cx-2, cx+3):
            for y in range(cy-2, cy+3):
                points.add((x, y))

        valid = False
        bubbles = []
        while not valid:
            seeds = random.sample(points, self.num_bubbles)
            borders = set()
            for seed in seeds:
                borders = borders.union(set(geometry.neighbors(seed)))

            ok = True
            for seed in seeds:
                if seed in borders:
                    ok = False

            if ok:
                valid = True
                for seed in seeds:
                    bubbles.append(
                        Bubble(seed, self, random.choice(self.target_areas),
                               random.choice(self.target_ratios))
                    )

        self.bubbles = bubbles

    def can_push(self, origin_bubble, direction):
        bubbles_affected = set()
        for point in origin_bubble.rect.edge(direction):
            # blocked points cannot be pushed
            if point in self.blocked:
                return False

            for bubble in self.bubbles:
                if bubble is origin_bubble:
                    continue

                if point in bubble.rect.border:
                    bubbles_affected.add(bubble)

        push_ok = True
        for bubble in bubbles_affected:
            push_ok = push_ok and bubble.can_be_pushed(direction)

        return push_ok

    def resolve_push(self, origin_bubble, direction):
        bubbles_affected = set()
        for point in origin_bubble.rect.edge(direction):
            # blocked points cannot be pushed
            if point in self.blocked:
                return False

            for bubble in self.bubbles:
                if bubble is origin_bubble:
                    continue

                if point in bubble.rect.border:
                    bubbles_affected.add(bubble)

        push_ok = True
        for bubble in bubbles_affected:
            push_ok = push_ok and bubble.move(direction)

        return push_ok

    def bubble_has_free_side(self, bubble, direction):
        all_boundaries = set()
        all_boundaries = all_boundaries.union(self.blocked)
        for bubble_ in self.bubbles:
            if bubble_ is bubble:
                continue
            all_boundaries = all_boundaries.union(set(bubble_.rect.border))

        edge = bubble.rect.edge(direction)
        for point in edge:
            if point in all_boundaries:
                return False

        return True

    def find_adjacent(self, room):
        pass


class Bubble:
    def __init__(self, pos, field, target_area, target_aspect_ratio):
        self.target_area = target_area
        self.target_aspect_ratio = target_aspect_ratio
        self.rect = geometry.Rectangle(pos, 1, 1)
        self.field = field
        self.can_expand = {
            geometry.Direction.north: True,
            geometry.Direction.south: True,
            geometry.Direction.east: True,
            geometry.Direction.west: True
        }

    def determine_axis_to_expand(self):
        north_south = [geometry.Direction.north, geometry.Direction.south]
        east_west = [geometry.Direction.east, geometry.Direction.west]

        def other_axis(axis_):
            if axis_ == north_south:
                return east_west
            else:
                return north_south

        if self.rect.width < self.rect.height:
            if self.rect.width/self.rect.height < self.target_aspect_ratio:
                axis = east_west
            else:
                axis = north_south

        else:
            if self.rect.height/self.rect.width < self.target_aspect_ratio:
                axis = north_south
            else:
                axis = east_west

        axis_ok = False
        for direction in axis:
            if self.can_expand[direction]:
                axis_ok = True

        if not axis_ok and self.rect.area() < self.target_area:
            return other_axis(axis)

        return axis

    def expand(self):
        if self.rect.area() > self.target_area:
            return False

        if not any(self.can_expand.values()):
            return False

        axis = self.determine_axis_to_expand()

        random.shuffle(axis)

        for direction in axis:
            if not self.can_expand[direction]:
                continue

            if self.field.bubble_has_free_side(self, direction):
                self.rect.grow(direction)
                return True

            elif self.field.can_push(self, direction):
                self.field.resolve_push(self, direction)
                self.rect.grow(direction)
                return True

            else:
                self.can_expand[direction] = False

        return False

    def move(self, direction):
        if self.field.bubble_has_free_side(self, direction):
            self.rect.move(direction)
            return True

        elif self.field.resolve_push(self, direction):
            self.rect.move(direction)
            return True

        else:
            return False

    def can_be_pushed(self, direction):
        if self.field.bubble_has_free_side(self, direction):
            return True

        elif self.field.can_push(self, direction):
            return True

        else:
            return False
