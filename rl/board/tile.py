import logging

from rl.ui import colors

class EntityPlacementException(Exception):
    pass

class Tile(object):
    def __init__(self, board, pos):
        self.pos = pos
        self.board = board
        self.has_been_seen = False
        self.visible = False
        self.remembered = ' '
        self.entities = {
            'obstacle': None,
            'actor': None,
            'items': [],
            'decorations': []
        }


    @property
    def obstacle(self):
        return self.entities['obstacle']

    @obstacle.setter
    def obstacle(self, val):
        self.entities['obstacle'] = val

    @property
    def actor(self):
        return self.entities['actor']

    @actor.setter
    def actor(self, val):
        self.entities['actor'] = val

    @property
    def items(self):
        return self.entities['items']

    @property
    def decorations(self):
        return self.entities['decorations']

    def blocks_movement(self):
        if (self.obstacle and
            self.obstacle.blocks_movement):
            return True

        if (self.actor and
            self.actor.blocks_movement):

            return True

        return False

    def blocks_vision(self):
        for k, ent in self.entities.items():
            if type(ent) == list:
                for o in ent:
                    if o and o.blocks_vision:
                        return True
            elif ent and ent.blocks_vision:
                return True

        return False

    def add_actor(self, ent):
        if self.actor is not None:
            raise EntityPlacementException("Tried to add an actor to a"
             "square that already has one")
        self.actor = ent

    def add_obstacle(self, ent):
        if self.obstacle is not None:
            raise EntityPlacementException("Tried to add an obstacle"
            "to a square that already has one")
        self.obstacle = ent

    def add_item(self, ent):
        for item in self.items:
            if type(ent) == type(item):
                item.stack_size += 1
                return

        self.items.append(ent)

    def remove_item(self, item, quantity=None):
        for i, item_ in enumerate(self.items):
            if type(item_) == type(item):
                if quantity and quantity <= item_.stack_size:
                    item_.stack_size -= quantity
                    if item_.stack_size == 0:
                        self.items.remove(item_)

                    return item_

                else:
                    self.items.remove(item_)
                    return item_


    def add_decoration(self, ent):
        if ent not in self.decorations:
            self.decorations.append(ent)

    def most_interesting_entity(self):
        most_interesting = None
        interest_level = 0

        ent = self.actor
        if ent and ent.interest_level > interest_level:
            most_interesting = ent
            interest_level = ent.interest_level

        ent = self.obstacle
        if ent and ent.interest_level > interest_level:
            most_interesting = ent
            interest_level = ent.interest_level

        for ent in self.items:
            if ent and ent.interest_level > interest_level:
                most_interesting = ent
                interest_level = ent.interest_level

        for ent in self.decorations:
            if ent and ent.interest_level > interest_level:
                most_interesting = ent
                interest_level = ent.interest_level

        return most_interesting

    def add_entity(self, ent):
        if ent.can_act:
            self.add_actor(ent)
        elif ent.blocks_movement:
            self.add_obstacle(ent)
        elif (ent.usable or ent.equippable):
            self.add_item(ent)
        else:
            self.add_decoration(ent)

    def remove_entity(self, ent):
        if ent.can_act and self.actor == ent:
            self.actor = None
        elif ent.blocks_movement and self.obstacle == ent:
            self.obstacle = None
        elif ent.can_be_taken and ent in self.items:
            self.remove_item(ent)
        elif ent in self.decorations:
            self.decorations.remove(ent)

    def remembered_glyph(self):
        glyph = '.'
        ent = None
        if self.actor:
            ent = self.actor

        elif self.obstacle:
            ent = self.obstacle

        elif self.items:
            ent = self.items[0]

        elif self.decorations:
            ent = self.decorations[0]

        if ent:
            glyph = ent.glyph

        return glyph

    def draw(self, force_visible=False):

        color = colors.light_gray
        bgcolor = None

        # debug
        # self.visible = True

        if self.visible or force_visible:
            glyph = '.'
            ent = None
            if self.actor:
                ent = self.actor

            elif self.obstacle:
                ent = self.obstacle

            elif self.items:
                ent = self.items[0]

            elif self.decorations:
                ent = self.decorations[0]

            if ent:
                glyph, color, bgcolor = ent.draw()

            self.remembered = glyph
        else:
            glyph = self.remembered
            color = colors.dark_gray
            bgcolor = colors.black

        return (glyph, color, bgcolor)


    def surrounding(self, as_dict=False):
        """returns up to 8 surrounding tiles, fewer if called from an
        edge or corner"""
        x, y = self.pos

        neighbors = [
            (x, y-1),   # north
            (x+1, y-1), # northeast
            (x+1, y),   # east
            (x+1, y+1), # southeast
            (x, y+1),   # south
            (x-1, y+1), # southwest
            (x-1, y),   # west
            (x-1, y-1), # northwest
        ]

        if as_dict:
            r = {}
            dirs = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
            for i, neighbor in enumerate(neighbors):
                d = dirs[i]
                if self.board.position_is_valid(neighbor):
                    r[d] = self.board[neighbor]

            return r

        return [self.board[neighbor] for neighbor in neighbors
            if self.board.position_is_valid(neighbor)]


    def on_first_seen(self):
        if self.actor:
            self.actor.on_first_seen()

        if self.obstacle:
            self.obstacle.on_first_seen()

        for item in self.items:
            item.on_first_seen()

        for decoration in self.decorations:
            decoration.on_first_seen()

    def adjacent(self, as_dict=False):
        """returns the 4 adjacent tiles, fewer if called from an edge or
        corner"""
        x, y = self.pos

        neighbors = [
            (x, y-1),   # north
            (x+1, y),   # east
            (x, y+1),   # south
            (x-1, y),   # west
        ]

        if as_dict:
            r = {}
            dirs = ['n', 'e', 's', 'w']
            for i, neighbor in enumerate(neighbors):
                d = dirs[i]
                if self.board.position_is_valid(neighbor):
                    r[d] = self.board[neighbor]

            return r

        return [self.board[neighbor] for neighbor in neighbors
            if self.board.position_is_valid(neighbor)]