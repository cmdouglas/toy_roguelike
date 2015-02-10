import textwrap

from rl.ui import colors

class Console(object):
    def __init__(self):
        self.messages = []
        
    def add_message(self, message, color=None, important=False):
        if not color:
            color=colors.white
        self.messages.append({
            'message': message,
            'color': color,
            'important': important
        })

    def get_last_lines(self, num_lines=4):
        last_messages = self.messages[-1*num_lines:]
        lines = []
        for message in reversed(last_messages):
            ls = textwrap.wrap(message['message'])
            for l in reversed(ls):
                lines.append({
                    'message': l,
                    'color': message['color'],
                    'important': False
                })
                                
                if message['important']:
                    lines[-1]['important'] = True
                    break
        
        return list(reversed(lines))[-1*num_lines:]
                    
