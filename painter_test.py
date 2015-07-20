import random
from rl.board.generator.painters.cave import CavePainter
from rl.board.generator.painters.shapedroom import RectangularRoomPainter, EllipticalRoomPainter, CircularRoomPainter
from rl.board.generator.painters.tunnel import SnakeyTunnelPainter, SimpleTunnelPainter
from rl.board.generator.painters.roomcluster import RoomClusterPainter

from rl.util.partition import Partition
from rl.board.generator.maparea import MapArea, LEFT, RIGHT
from rl.board.board import Board
from rl.util.geometry import Direction

width = 20
height = 20
painter_type = RoomClusterPainter

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
            'point': (width-1, random.randrange(1, height)),
            'side': RIGHT
        }
    ]
    painter = painter_type(board, area)

    painter.paint()

    print(painter.dumps())

if __name__ == '__main__':
    main()