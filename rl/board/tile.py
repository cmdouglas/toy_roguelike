import logging

from rl.ui import colors
from rl.util import geometry

logger = logging.getLogger('rl')


class EntityPlacementException(Exception):
    pass


class Tile(object):
    def __init__(self, board, pos):
        self.pos = pos
        self.board = board
        self.has_been_seen = False
        self.visible = False
        self.remembered = ' '
        self.remembered_desc = ''
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

    @property
    def all_entities(self):
        if self.actor:
            yield self.actor

        if self.obstacle:
            yield self.obstacle

        for item in self.items:
            yield item

        for decoration in self.decorations:
            yield decoration


    def blocks_movement(self):
        if self.obstacle and self.obstacle.blocks_movement:
            return True

        if self.actor and self.actor.blocks_movement:

            return True

        return False

    def is_closed_door(self):
        if (self.obstacle
            and self.obstacle.is_door
            and not self.obstacle.is_open):
            return True
        else:
            return False

    def blocks_vision(self):
        for ent in self.all_entities:
            if ent.blocks_vision:
                return True

        return False

    def add_actor(self, ent):
        if self.actor is not None:
            raise EntityPlacementException(
                "Tried to add an actor to a square that already has one"
            )
        self.actor = ent

    def add_obstacle(self, ent):
        if self.obstacle is not None:
            raise EntityPlacementException(
                "Tried to add an obstacle to a square that already has one"
            )
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

    def add_entity(self, ent):
        if ent.can_act:
            self.add_actor(ent)
        elif ent.blocks_movement:
            self.add_obstacle(ent)
        elif (ent.usable or ent.equippable):
            self.add_item(ent)
        else:
            self.add_decoration(ent)

        ent.tile = self

    def remove_entity(self, ent):
        if ent.can_act and self.actor == ent:
            self.actor = None
        elif ent.blocks_movement and self.obstacle == ent:
            self.obstacle = None
        elif ent.can_be_taken and ent in self.items:
            self.remove_item(ent)
        elif ent in self.decorations:
            self.decorations.remove(ent)

        ent.tile = None

    def remembered_glyph(self):
        glyph = '.'
        ents = list(self.all_entities)
        if ents:
            glyph = ents[0].glyph

        return glyph

    def get_visible_entity(self, force_visible=False):
        ent = None
        if self.visible or force_visible:
            ents = list(self.all_entities)
            if ents:
                ent = ents[0]

        return ent

    def remember_entity(self, ent):
        if ent:
            glyph, _, _ = ent.draw()
            self.remembered = glyph
            self.remembered_desc = ent.describe()
        else:
            self.remembered = '.'
            self.remembered_desc = ''

    def draw(self, force_visible=False):
        color = colors.light_gray
        bgcolor = None

        if self.visible or force_visible:
            glyph = '.'
            ent = self.get_visible_entity(force_visible=force_visible)
            if ent:
                glyph, color, bgcolor = ent.draw()

            self.remember_entity(ent)

        else:
            glyph = self.remembered
            color = colors.dark_gray
            bgcolor = colors.black

        return (glyph, color, bgcolor)

    def on_first_seen(self):
        for ent in self.all_entities:
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
            if (dx != 0 and dy != 0):
                continue

            point = (x+dx, y+dy)
            if self.board.position_is_valid(point):
                neighboring_tiles.append(self.board[point])
                neighboring_tiles_dict[d] = self.board[point]

        if as_dict:
            return neighboring_tiles_dict

        else:
            return neighboring_tiles
