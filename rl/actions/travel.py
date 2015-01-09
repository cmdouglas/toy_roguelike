import logging

from rl import globals as G
from rl.actions import action

class DirectionalTravelAction(action.Action):
    """A repeating movement action"""
    def __init__(self, actor, direction, last_surroundings=None):
        self.actor = actor
        self.direction = direction
        self.last_surroundings = last_surroundings

    def calculate_cost(self):
        dx, dy = self.direction

        if abs(dx) == 1 and abs(dy) ==1:
            #diagonal move, costs sqrt(2)
            return 1414

        else:
            return 1000

    def do_action(self):
        if not self.should_stop_travelling():
            last_surroundings = self.get_surroundings()
            success = self.actor.move(self.direction)
            if success:
                self.actor.queue_action(DirectionalTravelAction(self.actor, self.direction, last_surroundings=last_surroundings))

            return success, success

    def should_stop_travelling(self):
        # first check if movement is possible:
        cx, cy = self.actor.tile.pos
        dx, dy = self.direction
        new_pos = (cx+dx, cy+dy)

        if not G.world.board.position_is_valid(new_pos):
            return True

        if G.world.board[new_pos].blocks_movement():
            return True

        # next check for any visible hostiles:
        visible_mobs = [mob for mob in G.world.board.entities if mob.can_act and mob != self.actor and mob.is_in_fov()]

        if visible_mobs:
            return True

        # next check if we've hit a fork in the road
        if self.surroundings_have_changed_meaningfully(self.last_surroundings, self.get_surroundings()):
            return True

        return False


    def get_surroundings(self):
        """grabs a snapshot of what our immediate surroundings look like."""
        s = self.actor.tile.surrounding(as_dict=True)

        return {
            (-1, -1): self.main_feature(s['nw']),
            (-1, 0): self.main_feature(s['w']),
            (-1, 1): self.main_feature(s['sw']),
            (0, 1): self.main_feature(s['s']),
            (1, 1): self.main_feature(s['se']),
            (1, 0): self.main_feature(s['e']),
            (1, -1): self.main_feature(s['ne']),
            (0, -1): self.main_feature(s['n'])
        }

    def surroundings_have_changed_meaningfully(self, last_surroundings, current_surroundings):
        if not last_surroundings:
            return False
        new = self.new_surrounding_dirs()

        for d in new:
            if last_surroundings[d] != current_surroundings[d]:
                return True

        return False

    def new_surrounding_dirs(self):
        def _horizontal_directions(d):
            return [(d, -1), (d, 0), (d, 1)]

        def _vertical_directions(d):
            return[(-1, d), (0, d), (1, d)]

        dx, dy = self.direction
        s = []
        if dx:
            s.extend(_horizontal_directions(dx))

        if dy:
            s.extend(_vertical_directions(dy))

        return list(set(s))

    def main_feature(self, tile):
        if not tile.entities['obstacle']:
            return ' '

        if tile.entities['obstacle'].is_wall:
            return '#'

        if tile.entities['obstacle'].is_door:
            return '+'
