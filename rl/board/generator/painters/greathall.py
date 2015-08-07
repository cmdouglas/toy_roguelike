from rl.board.generator.painters import Painter

# TODO: reimplement this -- it was super boring as it was earlier
class GreatHallPainter(Painter):
    def paint(self):
        raise NotImplementedError()

    @classmethod
    def region_meets_requirements(cls, region):
        return region.width > 10 and region.height > 10