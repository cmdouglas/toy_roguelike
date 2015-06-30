
class MenuModeCommand():
   def __init__(self, mode):
       self.mode = mode


class MoveSelectedCommand(MenuModeCommand):
    def __init__(self, mode, d, n=1):
        super().__init__(mode)
        self.d = d
        self.n = n

    def process(self, menu):
        for i in range(self.n):
            if self.d == 1:
                menu.move_up()
            else:
                menu.move_down()
        self.mode.changed = True


class ExitMenuCommand(MenuModeCommand):
    def process(self, menu):
        self.mode.exit()


class SelectCommand(MenuModeCommand):
    def __init__(self, mode, key=None):
        super().__init__(mode)
        self.key = key

    def process(self, menu):
        selected = menu.get_selected(key=self.key)
        if selected:
            self.mode.handle_select(selected)
        self.mode.changed = True
