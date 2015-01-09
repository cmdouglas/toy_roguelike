"""Not really an AI, but this is how user controlled critters get their actions."""


class UserInput():
    def __init__(self, player):
        self.command = None
        self.player = player

    def set_command(self, command):
        self.command = command

    def get_action(self):
        if self.command:
            action = self.command.process(self.player)
            self.command=None
            return action