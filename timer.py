import time


class Timer(object):
    shouldBeRunning = False

    def __init__(self, tick, interval = 10):
        self.tick = tick
        self.interval = interval

    def start(self):
        self.shouldBeRunning = True
        print("Loop starting...")
        while self.shouldBeRunning:
            self.tick()
                
    def stop(self):
        self.shouldBeRunning = False