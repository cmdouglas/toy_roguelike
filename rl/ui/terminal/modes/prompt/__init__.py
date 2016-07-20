import unicodedata
from rl.ui.terminal.modes import Mode
from rl.ui.terminal.modes.prompt.layout import PromptModeLayout
from termapp.term import term


class PromptMode(Mode):
    def __init__(self, prompt="", max_length=0, on_entry=None):
        super().__init__()
        self.prompt = prompt
        self.text = ""
        self.max_length = max_length
        self.on_entry = on_entry
        self.layout = PromptModeLayout(self)
        self.changed = True

    def on_enter(self):
        self.owner.screen.clear()

    def next_frame(self):
        if self.changed:
            self.changed = False
            return self.layout.render()

    def handle_keypress(self, key):
        if key.code == term.KEY_ENTER:
            # accept the value
            if self.validate_text():
                self.accept_text()

        elif key.code in (term.KEY_BACKSPACE, term.KEY_DELETE):
            self.text = self.text[:-1]
            self.changed = True
            return

        elif key.is_sequence:
            return

        else:
            char = str(key)
            if unicodedata.category(char) in ['Cc', 'Cn']:
                return

            if self.max_length and len(self.text) >= self.max_length:
                return

            self.text += char
            self.changed = True
            return

    def validate_text(self):
        return self.text.strip() != ""

    def accept_text(self):
        if self.on_entry:
            self.on_entry(self.text.strip())

        self.exit()
