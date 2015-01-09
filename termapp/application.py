import asyncio
import blessed


t = blessed.Terminal()

class ScreenLine:
    def __init__(self):
        self.text = ""
        self.dirty = True


class Screen:
    def __init__(self):
        self.lines = [ScreenLine() for _ in range(t.height - 1)]

    def clear(self):
        for line in self.lines:
            line.text = " " * t.width
            line.dirty=True

    def refresh(self):
        for y, line in enumerate(self.lines):
            if line.dirty:
                with t.location(0, y):
                    print(line.text)

                line.dirty = False

    def update(self, frame):
        if not frame:
            return

        for screenline, newtext in zip(self.lines, frame):
            if screenline.text != newtext:
                screenline.text = newtext
                screenline.dirty = True


class StopApplication(Exception):
    pass


class TerminalApplication:
    def __init__(self, config=None):
        if not config:
            config={}
        self.term = t
        self.screen = Screen()
        self.loop = asyncio.get_event_loop()
        self.fps = config.get('fps', 30)

    def on_start(self):
        pass

    def newframe(self):
        yield

    def on_end(self):
        pass

    def handle_keypress(self, key):
        pass

    def run(self):
        @asyncio.coroutine
        def keyboard_input():

            k = self.term.inkey(timeout=0.005, esc_delay=0.005)
            if k:
                return self.handle_keypress(k)

        @asyncio.coroutine
        def animate():
            dt = 1/self.fps

            try:
                while True:
                    last_frame_at = self.loop.time()

                    yield from keyboard_input()
                    frame = self.newframe()
                    self.screen.update(frame)
                    self.screen.refresh()

                    wait = max(last_frame_at+dt - self.loop.time(), 0)
                    yield from asyncio.sleep(wait)

            except StopApplication:
                return

        self.on_start()
        with self.term.fullscreen(), self.term.hidden_cursor(), self.term.cbreak():
            self.loop.run_until_complete(animate())

        self.on_end()

