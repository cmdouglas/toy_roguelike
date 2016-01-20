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

#
# @rl_types.dumper(UserInput, 'user_input', 1)
# def _dump_user_input(user_input):
#     return ""
#
# @rl_types.loader('user_input', 1)
# def _load_user_input(data, version):
#     return UserInput()