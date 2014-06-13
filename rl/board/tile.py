import logging

from rl.io import colors

class GameObjectPlacementException(Exception):
    pass

class Tile(object):
    def __init__(self, board, pos):
        self.pos = pos
        self.board = board
        self.has_been_seen = False
        self.visible = False
        self.remembered = ' '
        self.objects = {
            'obstacle': None,
            'actor': None,
            'items': [],
            'decorations': []
        }

    def blocks_movement(self):
        if (self.objects['obstacle'] and
            self.objects['obstacle'].blocks_movement):
            return True

        if (self.objects['actor'] and
            self.objects['actor'].blocks_movement):

            return True

        return False

    def blocks_vision(self):
        for k, ob in self.objects.items():
            if type(ob) == list:
                for o in ob:
                    if o and o.blocks_vision:
                        return True
            elif ob and ob.blocks_vision:
                return True

        return False

    def add_actor(self, ob):
        if self.objects['actor'] is not None:
            raise GameObjectPlacementException("Tried to add an actor to a"
             "square that already has one")
        self.objects['actor'] = ob

    def add_obstacle(self, ob):
        if self.objects['obstacle'] is not None:
            raise GameObjectPlacementException("Tried to add an obstacle"
            "to a square that already has one")
        self.objects['obstacle'] = ob

    def add_item(self, ob):
        for item in self.objects['items']:
            if type(ob) == type(item):
                item.stack_size += 1
                return

        self.objects['items'].append(ob)

    def remove_item(self, item, quantity=None):
        for i, item_ in enumerate(self.objects['items']):
            if type(item_) == type(item):
                if quantity and quantity <= item_.stack_size:
                    item_.stack_size -= quantity
                    if item_.stack_size == 0:
                        self.objects['items'].remove(item_)

                    return item_

                else:
                    self.objects['items'].remove(item_)
                    return item_


    def add_decoration(self, ob):
        if ob not in self.objects['decorations']:
            self.objects['decorations'].append(ob)

    def most_interesting_object(self):
        most_interesting = None
        interest_level = 0

        ob = self.objects['actor']
        if ob and ob.interest_level > interest_level:
            most_interesting = ob
            interest_level = ob.interest_level

        ob = self.objects['obstacle']
        if ob and ob.interest_level > interest_level:
            most_interesting = ob
            interest_level = ob.interest_level

        for ob in self.objects['items']:
            if ob and ob.interest_level > interest_level:
                most_interesting = ob
                interest_level = ob.interest_level

        for ob in self.objects['decorations']:
            if ob and ob.interest_level > interest_level:
                most_interesting = ob
                interest_level = ob.interest_level

        return most_interesting

    def add_object(self, ob):
        if ob.can_act:
            self.add_actor(ob)
        elif ob.blocks_movement:
            self.add_obstacle(ob)
        elif ob.can_be_taken:
            self.add_item(ob)
        else:
            self.add_decoration(ob)

    def remove_object(self, ob):
        if ob.can_act and self.objects['actor'] == ob:
            self.objects['actor'] = None
        elif ob.blocks_movement and self.objects['obstacle'] == ob:
            self.objects['obstacle'] = None
        elif ob.can_be_taken and ob in self.objects['items']:
            self.remove_item(ob)
        elif ob in self.objects['decorations']:
            self.objects['decorations'].remove(ob)

    def remembered_char(self):
        char = '.'
        ob = None
        if self.objects['actor']:
            ob = self.objects['actor']

        elif self.objects['obstacle']:
            ob = self.objects['obstacle']

        elif self.objects['items']:
            ob = self.objects['items'][0]

        elif self.objects['decorations']:
            ob = self.objects['decorations'][0]

        if ob:
            char = ob.char

        return char

    def draw(self):

        color = colors.light_gray
        bgcolor = colors.black

        # debug
        # self.visible = True

        if self.visible:
            char = '.'
            ob = None
            if self.objects['actor']:
                ob = self.objects['actor']

            elif self.objects['obstacle']:
                ob = self.objects['obstacle']

            elif self.objects['items']:
                ob = self.objects['items'][0]

            elif self.objects['decorations']:
                ob = self.objects['decorations'][0]

            if ob:
                char, color, bgcolor = ob.draw()

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
        if self.objects['actor']:
            self.objects['actor'].on_first_seen()

        if self.objects['obstacle']:
            self.objects['obstacle'].on_first_seen()

        for item in self.objects['items']:
            item.on_first_seen()

        for decoration in self.objects['decorations']:
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