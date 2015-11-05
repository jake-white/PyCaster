import time


class Timer(object):
    shouldBeRunning = False

    def __init__(self, tick, interval = 10):
        self.tick = tick
        self.interval = interval

    def start(self):
        self.shouldBeRunning = True
        print("Loop starting...")
        self.timeSinceTick = self.interval
        currentTime = time.time()
        while self.shouldBeRunning:
            self.timeSinceTick = timeInMillis() - currentTime
            #print(timeElapsed)
            if self.timeSinceTick >= self.interval:
                self.tick()
                currentTime = timeInMillis()
                #print(currentTime)
                
    def stop(self):
        self.shouldBeRunning = False


def timeInMillis():
    return time.time() * 1000