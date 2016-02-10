import logging

from rl.util import geometry

logger = logging.getLogger('rl')


class EntityPlacementException(Exception):
    pass


class Tile(object):
    def __init__(self, board=None, pos=None):
        self.pos = pos
        self.board = board

        # entity layers
        self._terrain = None
        self._creature = None
        self._items = []

    @property
    def entities(self):
        yield self._creature
        yield self._terrain

        for item in self._items:
            yield item

    @property
    def terrain(self):
        return self._terrain

    @terrain.setter
    def terrain(self, new_terrain):
        if self._terrain:
            self._terrain.tile = None

        self._terrain = new_terrain
        new_terrain.tile = self

    @property
    def creature(self):
        return self._creature

    @creature.setter
    def creature(self, new_creature):
        if new_creature:
            if self._creature:
                raise EntityPlacementException("Cannot add creature to occupied tile")
            new_creature.tile = self
        self._creature = new_creature

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        self._items = items


    def add_item(self, new_item):
        for item in self.items:
            if type(new_item) == type(item):
                item.stack_size += 1
                return

        self.items.append(new_item)

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

    def blocks_movement(self):
        return any(ent.blocks_movement for ent in self.entities)

    def blocks_vision(self):
        return any(ent.blocks_vision for ent in self.entities)

    def on_first_seen(self):
        for ent in self.entities:
            ent.on_first_seen()

    def neighbors(self, as_dict=False):
        x, y = self.pos

        neighboring_tiles = []
        neighboring_tiles_dict = {}
        for d in geometry.Direction:
            dx, dy = d
            point = (x+dx, y+dy)
            if self.board.position_is_valid(point):
                neighboring_tiles.append(self.board[point])
                neighboring_tiles_dict[d] = self.board[point]

        if as_dict:
            return neighboring_tiles_dict

        else:
            return neighboring_tiles

    def adjacent(self, as_dict=False):
        x, y = self.pos

        neighboring_tiles = []
        neighboring_tiles_dict = {}
        for d in geometry.Direction:
            dx, dy = d
            if dx != 0 and dy != 0:
                continue

            point = (x+dx, y+dy)
            if self.board.position_is_valid(point):
                neighboring_tiles.append(self.board[point])
                neighboring_tiles_dict[d] = self.board[point]

        if as_dict:
            return neighboring_tiles_dict

        else:
            return neighboring_tiles

    def __getstate__(self):
        return {
            'pos': self.pos,
            'terrain': self.terrain,
            'creature': self.creature,
            'items': self.items
        }

    def __setstate__(self, state):
        self.pos = state['pos']
        self.terrain = state['terrain']
        self.creature = state['creature']
        self.items = state['items']

