from termapp.formatstring import FormatString
from termapp.layout import Pane
from termapp import colors

class PromptPane(Pane):

    def __init__(self, width, height, mode):
        super().__init__(width, height)

        self.mode = mode

    def draw_prompt(self):
        line = "{prompt}: {text}_".format(
            prompt=self.mode.prompt,
            text=self.mode.text
        )

        self.set_line(0, FormatString(line))

    def refresh(self):
        self.draw_prompt()