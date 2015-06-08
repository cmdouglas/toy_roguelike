"""Not really an AI, but this is how user controlled critters get their
actions."""

import logging



logger = logging.getLogger('rl')


class UserInput():
    def __init__(self, player):
        self.commands = []
        self.player = player

    def add_command(self, command):
        self.commands.append(command)

    def get_action(self):
        if self.commands:
            return self.commands.pop(0).process(self.player)

