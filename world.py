class World(object):
    coordList = list()
    def __init__(self, length, width):
        object.__init__(self)
        self.coordList = [[0 for _ in range(length)] for _ in range(width)]
        self.length = length
        self.width = width
    def getLength(self):
        return self.length
    def getWidth(self):
        return self.width
    def getCoords(self):
        return self.coordList
    def getCoordAt(self, x, y):
        return self.coordList[x][y]


class Player(object):
    #angle measurements are in radians
    angle = 0
    FOV = 1

    def __init__(self, x, y):
        object.__init__(self)
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y