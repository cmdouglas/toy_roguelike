import logging
from rl.ui import colors
from rl.ui import glyphs
from rl.entities.obstacles.wall import Wall
from rl.entities.obstacles import door

from rl import globals as G

class SmoothWall(Wall):
    """A wall that updates its glyph based on surrounding tiles"""
    color = colors.dark_gray
    glyph = u' '

    glyph_occluded = u' '
    glyph_pillar = glyphs.circle
    glyph_vwall = glyphs.vline
    glyph_hwall = glyphs.hline
    glyph_necorner = glyphs.ne
    glyph_nwcorner = glyphs.nw
    glyph_secorner = glyphs.se
    glyph_swcorner = glyphs.sw
    glyph_t_north = glyphs.tee_n
    glyph_t_south = glyphs.tee_s
    glyph_t_east = glyphs.tee_e
    glyph_t_west = glyphs.tee_w
    glyph_cross = glyphs.cross
    should_update = False
    description = 'The smooth stone wall is solid and unyielding.'

    def on_first_seen(self):
        self.should_update = True
        for neighbor in self.adjoining_smoothwalls().values():
            neighbor.should_update = True

    def draw(self):
        if self.should_update:
            self.update_glyph(vantage_point=G.world.player.tile.pos)
            self.should_update = False

        return (self.glyph, self.color, self.bgcolor)

    def choose_glyph(self, filled):
        if len(filled) == 8:
            return self.glyph_occluded

        elif self.hwall(filled):
            return self.glyph_hwall

        elif self.vwall(filled):
            return self.glyph_vwall

        elif self.necorner(filled):
            return self.glyph_necorner

        elif self.nwcorner(filled):
            return self.glyph_nwcorner

        elif self.secorner(filled):
            return self.glyph_secorner

        elif self.swcorner(filled):
            return self.glyph_swcorner

        elif self.t_north(filled):
            return self.glyph_t_north

        elif self.t_south(filled):
            return self.glyph_t_south

        elif self.t_east(filled):
            return self.glyph_t_east

        elif self.t_west(filled):
            return self.glyph_t_west

        elif self.cross(filled):
            return self.glyph_cross

        else:
            return self.glyph_pillar

    def update_glyph(self, vantage_point=None):
        # logging.debug('Updating Wall at %s', self.tile.pos)

        filled = list(self.adjoining_room_border_tiles().keys())
        glyph = self.choose_glyph(filled)

        if glyph == self.glyph_pillar and vantage_point:
            # there are no (visible) connections to this wall.  Try again and
            # pretend that the nearest neighbors are visible.
            nearest = self.nearest_neighbors(vantage_point)

            filled = list(
                self.adjoining_room_border_tiles(pretend_seen=nearest).keys()
            )
            glyph = self.choose_glyph(filled)

        self.glyph = glyph

    def nearest_neighbors(self, vantage_point):
        px, py = vantage_point
        x, y = self.tile.pos

        if px > x:
            if py > y:
                # vantage point is southeast
                return ['s', 'se', 'e']
            if py == y:
                # vantage point is due east
                return ['se', 'e', 'ne']
            if py < y:
                # vantage point is northeast
                return ['e', 'ne', 'n']

        if px == x:
            if py > y:
                # vantage point is due south
                return ['se', 's', 'sw']
            if py < y:
                # vantage point due north
                return ['nw', 'n', 'ne']

        if px < x:
            if py > y:
                # vantage point is southwest
                return ['s', 'sw', 'w']
            if py == y:
                # vantage point is due west
                return ['sw', 'w', 'nw']
            if py < y:
                # vantage point is northwest
                return ['w', 'nw', 'n']

    def adjoining_smoothwalls(self):
        neighbors = self.tile.surrounding(as_dict=True)
        r = {}
        for k, v in neighbors.items():
            if isinstance(v.obstacle, SmoothWall):
                r[k] = v.obstacle

        return r

    def adjoining_room_border_tiles(self, pretend_seen=None):
        if not pretend_seen:
            pretend_seen = []

        room_borders = [
            door.Door,
            SmoothWall
        ]
        neighbors = self.tile.surrounding(as_dict=True)
        r = {}
        for k, v in neighbors.items():
            # for purposes of drawing tiles, assume unseen tiles are empty.
            if (v.has_been_seen or k in pretend_seen):
                if (v.obstacle and type(v.obstacle) in room_borders):
                    r[k] = v

        return r

    def hwall(self, dirs):
        """returns true if self should be an hwall according to dirs

        Valid cases:

        d.d ###
        #cd #c#
        d.d d.d

        key . = empty
            # = filled
            c = char in question
            d = don't care
        """

        patterns = [
            {
                'empty': ['n', 's'],
                'filled': ['e'],
                'transformations': [self.h_reflect]
            },
            {
                'empty': ['s'],
                'filled': ['e', 'w', 'nw', 'n', 'ne'],
                'transformations': [self.v_reflect]
            }
        ]

        for pattern in patterns:
            if self.pattern_match(dirs, pattern):
                return True

        return False

    def vwall(self, dirs):
        """
        returns true if self should be a vwall according to dirs

        vwall is a rotation of hwall"""
        return self.hwall(self.l_rotate(dirs))

    def t_north(self, dirs):
        """returns true if self should be a north t-junction according to dirs

        Valid cases:

        .#d .#.
        #c# #c#
        d.d ###

        plus h-reflection of non-symetrical case
        """
        patterns = [
            {
                'empty': ['nw', 's'],
                'filled': ['n', 'e', 'w'],
                'transformations': [self.h_reflect]
            },
            {
                'empty': ['ne', 'nw'],
                'filled': ['n', 'e', 'w', 'sw', 's', 'se'],
                'transformations': []
            }
        ]

        for pattern in patterns:
            if self.pattern_match(dirs, pattern):
                return True

        return False

    def t_south(self, dirs):
        """returns true if self should be a south t-junction according to dirs

        this is a v-reflection of the t-north case"""
        return self.t_north(self.v_reflect(dirs))

    def t_east(self, dirs):
        """returns true if self should be an east t-junction according to dirs

        this is a r-rotation of the t-north case"""
        return self.t_north(self.l_rotate(dirs))

    def t_west(self, dirs):
        """returns true if self should be an east t-junction according to dirs

        this is a r-rotation of the t-north case"""
        return self.t_north(self.r_rotate(dirs))

    def necorner(self, dirs):
        """returns true if self should be a northeast corner according to dirs

        Valid cases:

        d.d ###
        #c. #c#
        d#d .##

        """
        patterns = [
            {
                'empty': ['n', 'e'],
                'filled': ['s', 'w'],
                'transformations': []
            },
            {
                'empty': ['sw'],
                'filled': ['w', 'nw', 'n', 'ne', 'e', 'se', 's'],
                'transformations': []
            }
        ]

        for pattern in patterns:
            if self.pattern_match(dirs, pattern):
                return True

        return False

    def nwcorner(self, dirs):
        """returns true if self should be a northwest corner according to dirs

        nwcorner is an l-rotation of necorner"""
        return self.necorner(self.r_rotate(dirs))

    def secorner(self, dirs):
        """returns true if self should be a southeast corner according to dirs

        secorner is an r-rotation of necorner"""
        return self.necorner(self.l_rotate(dirs))

    def swcorner(self, dirs):
        """returns true if self should be a southwest corner according to dirs

        swcorner is 2 r-rotations of necorner"""
        return self.necorner(self.l_rotate(self.l_rotate(dirs)))

    def cross(self, dirs):
        """returns true if self should be a cross according to dirs

        Valid cases:

        .#d
        #c#
        d#.

        """
        patterns = [
            {
                'empty': ['nw', 'se'],
                'filled': ['n', 'e', 's', 'w'],
                'transformations': [self.l_rotate]
            }
        ]

        for pattern in patterns:
            if self.pattern_match(dirs, pattern):
                return True

        return False

    def pattern_match(self, dirs, pattern):

        def contains_all(haystack, needles):
            for needle in needles:
                if needle not in haystack:
                    return False
            return True

        def contains_none(haystack, needles):
            for needle in needles:
                if needle in haystack:
                    return False
            return True

        for t in pattern['transformations'] + [None]:
            tdirs = dirs
            if t:
                tdirs = t(dirs)

            if (contains_all(tdirs, pattern['filled']) and
                contains_none(tdirs, pattern['empty'])):
                return True

        return False

    def h_reflect(self, dirs):
        dirtrans = {
            'n': 'n',
            'ne': 'nw',
            'e': 'w',
            'se': 'sw',
            's': 's',
            'sw': 'se',
            'w': 'e',
            'nw': 'ne'
        }

        return [dirtrans[d] for d in dirs]

    def v_reflect(self, dirs):
        dirtrans = {
            'n': 's',
            'ne': 'se',
            'e': 'e',
            'se': 'ne',
            's': 'n',
            'sw': 'nw',
            'w': 'w',
            'nw': 'sw'
        }

        return [dirtrans[d] for d in dirs]

    def l_rotate(self, dirs):
        dirtrans = {
            'n': 'w',
            'ne': 'nw',
            'e': 'n',
            'se': 'ne',
            's': 'e',
            'sw': 'se',
            'w': 's',
            'nw': 'sw'
        }

        return [dirtrans[d] for d in dirs]

    def r_rotate(self, dirs):
        dirtrans = {
            'n': 'e',
            'ne': 'se',
            'e': 's',
            'se': 'sw',
            's': 'w',
            'sw': 'nw',
            'w': 'n',
            'nw': 'ne'
        }

        return [dirtrans[d] for d in dirs]
