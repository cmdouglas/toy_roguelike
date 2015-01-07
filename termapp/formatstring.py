import re
from wcwidth import wcswidth
from termapp import colors
from termapp import term

t = term.term

normal = '\x1b(B\x1b[m'

class Format:
    __slots__ = ['color', 'bgcolor']

    def __init__(self, color=None, bgcolor=None):
        self.color = color
        self.bgcolor = bgcolor

    def __eq__(self, other):
        return (
            self.color == other.color
            and self.bgcolor == other.bgcolor
        )

    def apply_to(self, s: str):
        formats = []
        if self.color is not None:
            formats.append(colors.color_codes[self.color])

        if self.bgcolor is not None:
            formats.append(colors.bgcolor_codes[self.bgcolor])

        if formats:
            formats.append(s)
            formats.append(normal)
            s = "".join(formats)

        return s


class FormatStringChunk:
    __slots__ = ['s', 'format']

    def __init__(self, s: str, fmt=None):
        self.s = s
        if fmt:
            self.format = fmt

        else:
            self.format = Format()

    def __str__(self):
        return self.format.apply_to(self.s)

    def __len__(self):
        return len(self.s)

    def __getitem__(self, item):
        return FormatStringChunk(self.s[item], self.format)

    def width(self):
        return wcswidth(self.s)

    def lines(self):
        for line in self.s.split("\n"):
            yield FormatStringChunk(line, fmt=self.format)

    def fs_repr(self):
        def escape(s):
            return s.replace('\\', r'\\').replace('[', '\[').replace(']', '\]')

        format_string = ""
        if self.format.color is not None:
            format_string += colors.color_names[self.format.color]

        if self.format.bgcolor is not None:
            format_string += colors.bg_color_names[self.format.bgcolor]

        if format_string:
            return "[{format_string}:{s}]".format(format_string=format_string, s=escape(self.s))

        return escape(self.s)

    def chars(self):
        for char in self.s:
            yield FormatStringChunk(char, self.format)

    def split_at(self, i: int):
        return self[:i], self[i:]


class FormatString:
    __slots__ = ['condensed', 'chunks']
    def __init__(self, data=None):
        self.condensed = False

        if not data:
            self.chunks = []
            return

        if type(data) == str:
            self.parse(data)

        elif type(data) == FormatStringChunk:
            self.chunks = [data]

        elif type(data) == FormatString:
            self.chunks = data.chunks

    def simple(self, s:str, color=None, bgcolor=None):
        fmt = Format(color=color, bgcolor=bgcolor)
        chunk = FormatStringChunk(s, fmt=fmt)
        self.chunks = [chunk]
        return self

    def condense(self):
        if self.condensed:
            return

        if not self.chunks:
            return

        first_chunk = self.chunks[0]
        current_format = first_chunk.format
        current_string = [first_chunk.s]
        newchunks = []

        for chunk in self.chunks[1:]:
            if chunk.format == current_format:
                current_string.append(chunk.s)

            else:
                newchunks.append(FormatStringChunk("".join(current_string), current_format))
                current_format = chunk.format
                current_string = [chunk.s]

        newchunks.append(FormatStringChunk("".join(current_string), current_format))
        self.chunks = newchunks

        self.condensed = True

    def __add__(self, other):
        new = FormatString()
        new.chunks = self.chunks[:]

        if type(other) == str:
            other = FormatString(other)
            new.chunks.extend(other.chunks)

        elif type(other) == FormatStringChunk:
            new.chunks.append(other)

        elif type(other) == FormatString:
            new.chunks.extend(other.chunks)

        else:
            raise TypeError()

        return new

    def __str__(self):
        self.condense()
        return "".join([str(chunk) for chunk in self.chunks])

    def __len__(self):
        return sum([len(chunk) for chunk in self.chunks])

    def __eq__(self, other):
        return str(self) == str(other)

    # TODO: optimize this if necessary
    def __getitem__(self, item):
        chars = list(self.chars())
        return FormatString.join("", chars[item])

    # TODO: optimize this if necessary
    def __setitem__(self, key, value):
        value = FormatString(value)
        chars = list(self.chars())
        if type(key) == slice:
            chars[key] = list(value.chars())
        else:
            chars[key] = value

        chunks = []
        for char in chars:
            chunks.extend(char.chunks)

        self.chunks = chunks

    def __repr__(self):
        self.condense()

        quotes = '"'
        if self.is_multiline():
            quotes = '"""'
        return '{classname}({quotes}{chunks}{quotes})'.format(
            classname=self.__class__.__qualname__,
            chunks=("".join([chunk.fs_repr() for chunk in self.chunks])),
            quotes=quotes
        )

    def lines(self):
        current_line = FormatString()
        for chunk in self.chunks:
            last_line = 0
            for i, line in enumerate(chunk.lines()):
                if i > last_line:
                    yield current_line
                    current_line = FormatString()
                else:
                    last_line = i

                current_line += line

        yield current_line

    def chars(self):
        for chunk in self.chunks:
            for char in chunk.chars():
                yield FormatString(char)

    def width(self):
        if self.is_multiline():
            return max([line.width() for line in self.lines()])
        else:
            return sum([chunk.width() for chunk in self.chunks])

    def ljust(self, width, fillchar=" "):
        lines = []
        for line in self.lines():
            fs = FormatString()
            offset = width - line.width()
            chunks = line.chunks[:]

            if offset > 0:
                fill = FormatStringChunk(offset*fillchar)
                chunks.append(fill)

            fs.chunks.extend(chunks)
            lines.append(fs)

        return FormatString.join("\n", lines)

    def rjust(self, width, fillchar=" "):
        lines = []
        for line in self.lines():
            fs = FormatString()
            offset = width - line.width()
            chunks = line.chunks[:]

            if offset > 0:
                fill = FormatStringChunk(offset*fillchar)
                chunks.insert(0, fill)

            fs.chunks.extend(chunks)
            lines.append(fs)

        return FormatString.join("\n", lines)

    @classmethod
    def join(cls, glue, pieces):

        if not pieces:
            return FormatString("")

        fs = FormatString()

        if glue:
            glue = FormatString(glue)

        for piece in pieces[:-1]:
            piece = FormatString(piece)
            fs.chunks.extend(piece.chunks)
            if glue:
                fs.chunks.extend(glue.chunks)

        pieces[-1] = FormatString(pieces[-1])
        fs.chunks.extend(pieces[-1].chunks)

        return fs

    def is_multiline(self):
        for chunk in self.chunks:
            if chunk.s.find("\n") != -1:
                return True

        return False

    # now I have two problems
    format_pattern = re.compile(
        r'(?<!\\)(?:\\\\)*\[(?P<color>' +
        '|'.join(colors.colors.keys()) +
        r')?(?P<bgcolor>' +
        '|'.join(colors.bg_colors.keys()) +
        r')?:(?P<text>.*?)(?<!\\)(?:\\\\)*\]',
        re.MULTILINE | re.DOTALL)

    def parse(self, string: str):
        """
        Parses simple formatting markup in the form:
        "text text text [<color><on_color>:formatted text] more text"

        Markup cannot be nested. Use backslashes to escape brackets/backslashes.

        >>> s = FormatString()
        >>> s.parse("[red:This is red.] This is not.")
        >>> str(s)
        '\x1b[91mThis is red.\x1b(B\x1b[m This is not.'
        >>> s.parse("Here is a red closing bracket: [red:\]]")
        >>> str(s)
        'Here is a red closing bracket: \x1b[91m]\x1b(B\x1b[m'
        """

        # don't actually parse if it's not necessary
        if '[' not in string and ']' not in string and '\\' not in string:
            self.chunks = [FormatStringChunk(string)]
            return

        def unescape(s: str):
            return s.replace('\[', '[').replace('\]', ']').replace(r'\\', '\\')

        chunks = []
        last = 0

        for match in re.finditer(FormatString.format_pattern, string):
            start, end = match.span()
            unformatted = string[last:start]

            if unformatted:
                chunks.append(FormatStringChunk(unescape(unformatted)))

            d = match.groupdict()
            f = Format()
            if d['color']:
                f.color = colors.colors[d['color']]

            if d['bgcolor']:
                f.bgcolor = colors.bg_colors[d['bgcolor']]
            chunks.append(FormatStringChunk(unescape(d['text']), f))
            last = end

        unformatted = string[last:]
        if unformatted:
            chunks.append(FormatStringChunk(unescape(unformatted)))

        self.chunks = chunks
