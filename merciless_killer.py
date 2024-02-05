import os
import signal


class MercilessKiller:
    def __init__(self):
        self.callbacks = []
        signal.signal(signal.SIGINT, self.kill)
        signal.signal(signal.SIGTERM, self.kill)

    def kill(self, *_):
        os.kill(os.getpid(), 9)
