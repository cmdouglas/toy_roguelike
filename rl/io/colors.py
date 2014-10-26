import sys
import itertools
from rl.util import tools

black       = 0
dark_red    = 1
green       = 2
sepia       = 3
dark_blue   = 4
purple      = 5
cyan        = 6
light_gray  = 7
dark_gray   = 8
red         = 9
light_green = 10
yellow      = 11
blue        = 12
magenta     = 13
light_cyan  = 14
white       = 15

class ColorException(Exception):
    pass

class ColorString(object):
    colors = [
        '\033[30m', '\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[37m',
        '\033[90m', '\033[91m', '\033[92m', '\033[93m', '\x1b[94m', '\033[95m', '\033[96m', '\033[97m'
    ]

    bgcolors = [
        '\033[40m', '\033[41m', '\033[43m', '\033[43m', '\033[44m', '\033[45m', '\033[46m', '\033[47m',
        '\033[100m', '\033[101m', '\033[102m', '\033[103m', '\033[104m', '\033[105m', '\033[106m', '\033[107m'
    ]

    clear = '\x1b(B\x1b[m'

    def __init__(self, s, color_data=None):
        """
        parameters:
            s: a string
            color_data: a list of tuples (from, to, color, <bg>)
                from, to: the substring you want the color applied to
                color: an int from 0-15 representing the color applied
                bg: optional boolean (default: false) indicates if this is a background color
        """
        self.s = s
        self.color_data = []
        if color_data:
            self.set_color_data(color_data)

    def add_color(self, color, start=0, end=None, length=None):
        if length is not None and end is None:
            end=start+length

        elif end is None:
            end = len(self.s)

        self.color_data.append((start, end, color, False))
        return self

    def add_bgcolor(self, color, start=0, end=None, length=None):
        if length is not None and end is None:
            end=start+length

        elif end is None:
            end = len(self.s)

        self.color_data.append((start, end, color, True))
        return self

    def set_color_data(self, data):
        cd = []
        for item in data:
            if len(item) == 3:
                start, end, color = item
                bg = False

            elif len(item) == 4:
                start, end, color, bg = item

            else:
                raise ColorException("Invalid color data item: {item}".format(item=item))


            cd.append((start, end, int(color), bool(bg)))

        self.color_data = cd

    def __iter__(self):
        return iter(self.s)

    def __str__(self):

        # make this encode to bytes if python version < 3
        # p.s.  UGH
        def encode(s):
            if (sys.version_info < (3,)):
                return s.encode('utf-8')
            else:
                return s

        points = []
        r = []

        STRING_START    = 0
        COLOR_END       = 1
        BGCOLOR_END     = 2
        COLOR_START     = 3
        BGCOLOR_START   = 4
        STRING_END      = 5

        for item in self.color_data:
            start, end, color, bg = item

            if start == end:
                # don't include color data for 0 length substrings
                continue

            points.append((start, BGCOLOR_START if bg else COLOR_START, color))
            points.append((end, BGCOLOR_END if bg else COLOR_END, color))

        points = [(0, STRING_START, -1)] + sorted(points) + [(len(self.s), STRING_END, -1)]

        for pointpair in tools.pairwise(points):
            ps, pe = pointpair
            start, code, color = ps
            end, _, _, = pe

            if code == STRING_START:
                r.append(encode(self.s[start:end]))

            elif code == COLOR_START:
                r.extend([self.colors[color], encode(self.s[start:end])])

            elif code == BGCOLOR_START:
                r.extend([self.bgcolors[color], encode(self.s[start:end])])

            elif code == COLOR_END:
                # switch to default color(white)
                r.extend([self.colors[light_gray], encode(self.s[start:end])])

            elif code == BGCOLOR_END:
                # switch to default background color(black)
                r.extend([self.bgcolors[black], encode(self.s[start:end])])

        r.append(self.clear)

        return "".join(r)

    def __add__(self, other):
        if type(other) is str:
            return ColorString(self.s + other, color_data=self.color_data)
        elif type(other) is ColorString:
            s = self.s + other.s
            cd = self.color_data[:].extend(other.offset_color_data(len(self)))

            return ColorString(s, color_data=cd)

        else:
            raise TypeError(
                "ColorStrings can only be concatinated with strings and other ColorStrings. "
                "Recieved {thing}".format(thing=str(type(other))))

    def __len__(self):
        return len(self.s)

    def ljust(self, width, fillchar=' '):
        return ColorString(self.s.ljust(width, fillchar), color_data=self.color_data)

    def rjust(self, width, fillchar=' '):
        offset = width - len(self)
        cd = self.offset_color_data(self)
        return ColorString(self.s.rjust(width, fillchar), color_data=cd)

    def offset_color_data(self, offset):
        r = []
        for item in self.color_data:
            start, end, color, bg = item
            r.append((start+offset, end+offset, color, bg))

        return r

    @classmethod
    def join(cls, glue, pieces):
        string_pieces = []
        color_data = []
        offset = 0

        # create an iterator with glue interleaved between all the pieces
        chunks = list(itertools.chain.from_iterable([(piece, glue) for piece in pieces]))[:-1]

        for chunk in chunks:
            if type(chunk) == str:
                string_pieces.append(chunk)

            elif type(chunk) == ColorString:
                string_pieces.append(chunk.s)
                color_data.extend(chunk.offset_color_data(offset))

            offset += len(chunk)

        return ColorString("".join(string_pieces), color_data=color_data)







