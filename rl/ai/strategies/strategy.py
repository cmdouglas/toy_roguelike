CONTINUE = 0
COMPLETE = 1
INTERRUPTED = 2


class Strategy(object):
    def do_strategy(self, actor, world):
        pass

    def describe(self):
        return ""
