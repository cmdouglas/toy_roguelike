import random

from rl.board.generator.painters.roomcluster import RoomClusterPainter
from rl.util.partition import Partition
from rl.board.region import MapRegion
from rl.board.board import Board
from termapp.formatstring import FormatString

width = 20
height = 20
painter_type = RoomClusterPainter
#painter_type = SnakeyTunnelPainter

def tile_is_empty(tile):
    return tile.terrain is None

def main():
    partition = Partition((0, 0), width, height)
    board = Board(width, height)
    area = MapArea(partition, board)
    area.connections = [
        {
            'area': None,
            'point': (0, random.randrange(1, height)),
            'side': LEFT
        },
        {
            'area': None,
            'point': (random.randrange(1, width), 0),
            'side': TOP
        },
        {
            'area': None,
            'point': (width-1, random.randrange(1, height)),
            'side': RIGHT
        }
    ]
    painter = painter_type(board, area)

    painter.paint()
    for row in board.tiles:
        for tile in row:
            if tile_is_empty(tile):
                tile.visible = True
                tile.has_been_seen = True
            for n in tile.neighbors():
                if tile_is_empty(n):
                    tile.visible = True
                    tile.has_been_seen = True


    out = []
    for tilerow in board.tiles:
        s = []
        for tile in tilerow:
            char, color, bgcolor = tile.draw()
            c = FormatString().simple(char, color, bgcolor)
            s.append(c)
        out.append(FormatString.join("", s))





    print(FormatString.join("\n", out))

if __name__ == '__main__':
    main()
