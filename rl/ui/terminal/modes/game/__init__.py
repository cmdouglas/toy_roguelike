from rl.ui.terminal.modes import Mode
from rl.ui.terminal.modes.prompt import PromptMode
from rl.ui.terminal.modes.world import WorldMode
from rl.world import World


class GameMode(Mode):
    def __init__(self, world=None):
        super().__init__()
        self.playing = False
        self.world = world
        if not self.world:
            self.world = World()

    def next_frame(self):
        if not self.world.generated:
            def on_entry(text):
                name = text
                self.world.generate(player_name=name)

            self.owner.enter_mode(PromptMode(prompt="Please enter your name", max_length=16, on_entry=on_entry))

        elif not self.playing:
            self.owner.enter_mode(WorldMode(self.world))
            self.playing = True

        else:
            self.exit()