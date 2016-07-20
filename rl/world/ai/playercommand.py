"""Not really an AI, but this is how user controlled critters get their
actions."""

import logging
#from rl.world.save import rl_types


logger = logging.getLogger('rl')


class UserInput():
    def __init__(self, actor=None):
        self.commands = []
        self.actor = actor

    def add_command(self, command):
        self.commands.append(command)

    def get_action(self):
        if self.commands:
            return self.commands.pop(0).process()

    def __setstate__(self, state):
        return {}

    def restore(self, actors_by_id):
        pass
