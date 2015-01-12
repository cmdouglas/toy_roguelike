import logging
from rl.ui import colors
from rl.ui import glyphs
from rl.entities.obstacles.wall import Wall
from rl.entities.obstacles import door

class SmoothWall(Wall):
    """A wall that updates its glyph based on surrounding tiles"""
    color=colors.dark_gray
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
            self.update_glyph()
            self.should_update =False

        return (self.glyph, self.color, self.bgcolor)
    
    def update_glyph(self):
        # logging.debug('Updating Wall at %s', self.tile.pos)
        
        filled = list(self.adjoining_room_border_tiles().keys())
               
        if len(filled) == 8:
            self.glyph = self.glyph_occluded
        
        elif self.hwall(filled):
            self.glyph = self.glyph_hwall
            
        elif self.vwall(filled):
            self.glyph = self.glyph_vwall
            
        elif self.necorner(filled):
            self.glyph = self.glyph_necorner
    
        elif self.nwcorner(filled):
            self.glyph = self.glyph_nwcorner
            
        elif self.secorner(filled):
            self.glyph = self.glyph_secorner
            
        elif self.swcorner(filled):
            self.glyph = self.glyph_swcorner
                    
        elif self.t_north(filled):
            self.glyph = self.glyph_t_north
            
        elif self.t_south(filled):
            self.glyph = self.glyph_t_south
            
        elif self.t_east(filled):
            self.glyph = self.glyph_t_east
            
        elif self.t_west(filled):
            self.glyph = self.glyph_t_west
            
        elif self.cross(filled):
            self.glyph = self.glyph_cross

        else:
            self.glyph = self.glyph_pillar

    def adjoining_smoothwalls(self):
        neighbors = self.tile.surrounding(as_dict=True)
        r = {}
        for k, v in neighbors.items():
            if isinstance(v.entities['obstacle'], SmoothWall):
                r[k] = v.entities['obstacle']

        return r

    def adjoining_room_border_tiles(self):
        neighbors = self.tile.surrounding(as_dict=True)
        r = {}
        for k, v in neighbors.items():
            #if :
            # for purposes of drawing tiles, assume unseen tiles are empty.
            if ((isinstance(v.entities['obstacle'], SmoothWall)
                or isinstance(v.entities['obstacle'], door.Door))
                and v.has_been_seen):
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