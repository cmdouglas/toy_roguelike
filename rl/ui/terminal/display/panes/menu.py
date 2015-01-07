from termapp.formatstring import FormatString
from termapp.layout import Pane
from termapp import colors

class MenuPane(Pane):

    def __init__(self, width, height, menu):
        super(MenuPane, self).__init__(width, height)

        self.menu = menu

    def draw_menu(self):
        if self.menu.items:
            for i, line in enumerate(self.menu.get_lines()):
                if line['selected']:
                    self.set_line(i, FormatString().simple(line['line'], color=colors.black, bgcolor=line['color']))
                else:
                    self.set_line(i, FormatString().simple(line['line'], color=line['color']))

        else:
            self.set_line(0, FormatString().simple(self.menu.empty))

    def refresh(self):
        self.draw_menu()