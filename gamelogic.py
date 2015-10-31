import time


class GameLoop(object):
    shouldBeRunning = True
    interval = 10

    def __init__(self, screen):
        # requires a looping interval (ms) and a screen object
        self.screen = screen

    def start(self):
        print("Loop starting...")
        self.timeSinceTick = self.interval
        currentTime = time.time()
        while self.shouldBeRunning:
            self.timeSinceTick = timeInMillis() - currentTime
            #print(timeElapsed)
            if (self.timeSinceTick >= self.interval):
                self.tick()
                currentTime = timeInMillis()
            #print(currentTime)

    def stop(self):
        self.shouldBeRunning = False

    def tick(self):
        self.screen.draw()

    def getInterval(self):
        return self.interval

    def getTimeSinceTick(self):
        return self.timeSinceTick


def timeInMillis():
    return time.time() * 1000
