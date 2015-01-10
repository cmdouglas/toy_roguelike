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

    def blocks_movement(self):
        if (self.entities['obstacle'] and
            self.entities['obstacle'].blocks_movement):
            return True

        if (self.entities['actor'] and
            self.entities['actor'].blocks_movement):

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
        if self.entities['actor'] is not None:
            raise EntityPlacementException("Tried to add an actor to a"
             "square that already has one")
        self.entities['actor'] = ent

    def add_obstacle(self, ent):
        if self.entities['obstacle'] is not None:
            raise EntityPlacementException("Tried to add an obstacle"
            "to a square that already has one")
        self.entities['obstacle'] = ent

    def add_item(self, ent):
        for item in self.entities['items']:
            if type(ent) == type(item):
                item.stack_size += 1
                return

        self.entities['items'].append(ent)

    def remove_item(self, item, quantity=None):
        for i, item_ in enumerate(self.entities['items']):
            if type(item_) == type(item):
                if quantity and quantity <= item_.stack_size:
                    item_.stack_size -= quantity
                    if item_.stack_size == 0:
                        self.entities['items'].remove(item_)

                    return item_

                else:
                    self.entities['items'].remove(item_)
                    return item_


    def add_decoration(self, ent):
        if ent not in self.entities['decorations']:
            self.entities['decorations'].append(ent)

    def most_interesting_entity(self):
        most_interesting = None
        interest_level = 0

        ent = self.entities['actor']
        if ent and ent.interest_level > interest_level:
            most_interesting = ent
            interest_level = ent.interest_level

        ent = self.entities['obstacle']
        if ent and ent.interest_level > interest_level:
            most_interesting = ent
            interest_level = ent.interest_level

        for ent in self.entities['items']:
            if ent and ent.interest_level > interest_level:
                most_interesting = ent
                interest_level = ent.interest_level

        for ent in self.entities['decorations']:
            if ent and ent.interest_level > interest_level:
                most_interesting = ent
                interest_level = ent.interest_level

        return most_interesting

    def add_entity(self, ent):
        if ent.can_act:
            self.add_actor(ent)
        elif ent.blocks_movement:
            self.add_obstacle(ent)
        elif ent.can_be_taken:
            self.add_item(ent)
        else:
            self.add_decoration(ent)

    def remove_entity(self, ent):
        if ent.can_act and self.entities['actor'] == ent:
            self.entities['actor'] = None
        elif ent.blocks_movement and self.entities['obstacle'] == ent:
            self.entities['obstacle'] = None
        elif ent.can_be_taken and ent in self.entities['items']:
            self.remove_item(ent)
        elif ent in self.entities['decorations']:
            self.entities['decorations'].remove(ent)

    def remembered_char(self):
        char = '.'
        ent = None
        if self.entities['actor']:
            ent = self.entities['actor']

        elif self.entities['obstacle']:
            ent = self.entities['obstacle']

        elif self.entities['items']:
            ent = self.entities['items'][0]

        elif self.entities['decorations']:
            ent = self.entities['decorations'][0]

        if ent:
            char = ent.char

        return char

    def draw(self, force_visible=False):

        color = colors.light_gray
        bgcolor = None

        # debug
        # self.visible = True

        if self.visible or force_visible:
            char = '.'
            ent = None
            if self.entities['actor']:
                ent = self.entities['actor']

            elif self.entities['obstacle']:
                ent = self.entities['obstacle']

            elif self.entities['items']:
                ent = self.entities['items'][0]

            elif self.entities['decorations']:
                ent = self.entities['decorations'][0]

            if ent:
                char, color, bgcolor = ent.draw()

            self.remembered = char
        else:
            char = self.remembered
            color = colors.dark_gray
            bgcolor = colors.black

        return (char, color, bgcolor)


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
        if self.entities['actor']:
            self.entities['actor'].on_first_seen()

        if self.entities['obstacle']:
            self.entities['obstacle'].on_first_seen()

        for item in self.entities['items']:
            item.on_first_seen()

        for decoration in self.entities['decorations']:
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