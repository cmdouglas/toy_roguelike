from rl.io import colors
from rl.io import chars
from rl.objects.obstacles.wall import Wall
from rl.objects.obstacles import door

class SmoothWall(Wall):
    """A wall that updates its glyph based on surrounding tiles"""
    color=colors.dark_gray
    char = u' '
    
    char_occluded = u' '
    char_pillar = chars.vline
    char_vwall = chars.vline
    char_hwall = chars.hline
    char_necorner = chars.ne
    char_nwcorner = chars.nw
    char_secorner = chars.se
    char_swcorner = chars.sw
    char_t_north = chars.tee_n
    char_t_south = chars.tee_s
    char_t_east = chars.tee_e
    char_t_west = chars.tee_w
    char_cross = chars.cross
    description = 'The smooth stone wall is solid and unyielding.'
    
    def on_spawn(self):
        self.update_char()
        for tile in list(self.adjoining_smoothwalls().values()):
            tile.objects['obstacle'].update_char()
            
    def on_despawn(self):
        for tile in list(self.adjoining_smoothwalls().values()):
            tile.objects['obstacle'].update_char()
    
    def update_char(self):
        # logging.debug('Updating Wall at %s', self.tile.pos)
        
        dirs = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        neighbors = list(self.tile.surrounding(as_dict=True).keys())
        filled = list(self.adjoining_room_border_tiles().keys())
        
        # if we're up against the edge of the map, assume
        # all non-present tiles are filled
        if len(neighbors) < 8:
            for d in dirs:
                if d not in neighbors:
                    filled.append(d)
               
        if len(filled) == 8:
            self.char = self.char_occluded
        
        elif len(filled) == 0:
            self.char = self.char_pillar
        
        elif self.hwall(filled):
            self.char = self.char_hwall
            
        elif self.vwall(filled):
            self.char = self.char_vwall
            
        elif self.necorner(filled):
            self.char = self.char_necorner
    
        elif self.nwcorner(filled):
            self.char = self.char_nwcorner
            
        elif self.secorner(filled):
            self.char = self.char_secorner
            
        elif self.swcorner(filled):
            self.char = self.char_swcorner
                    
        elif self.t_north(filled):
            self.char = self.char_t_north
            
        elif self.t_south(filled):
            self.char = self.char_t_south
            
        elif self.t_east(filled):
            self.char = self.char_t_east
            
        elif self.t_west(filled):
            self.char = self.char_t_west
            
        elif self.cross(filled):
            self.char = self.char_cross
        
    def adjoining_smoothwalls(self):
        neighbors = self.tile.surrounding(as_dict=True)
        r = {}
        for k, v in neighbors.items():
            if isinstance(v.objects['obstacle'], SmoothWall):
                r[k] = v
        
        return r

    def adjoining_room_border_tiles(self):
        neighbors = self.tile.surrounding(as_dict=True)
        r = {}
        for k, v in neighbors.items():
            if isinstance(v.objects['obstacle'], SmoothWall) or isinstance(v.objects['obstacle'], door.Door):
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