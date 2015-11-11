import math


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distanceTo(self, point):
        #d^2 = x^2 + y^2
        return math.sqrt(math.pow(self.y - point.y, 2) + math.pow((self.x - point.x), 2))

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def increaseY(self, increment):
        self.y += increment

    def increaseX(self, increment):
        self.x += increment

    def toString(self):
        return "({}, {})".format(self.x, self.y)
