class World(object):
    coordList = list()
    def __init__(self, length, width, playerX, playerY):
        object.__init__(self)
        self.coordList = [[0 for _ in range(length)] for _ in range(width)]
        self.length = length
        self.width = width
        self.player = Player(playerX, playerY)
    def getLength(self):
        return self.length

    def getWidth(self):
        return self.width

    def getCoords(self):
        return self.coordList

    def getCoordAt(self, x, y):
        return self.coordList[x][y]

    def getPlayer(self):
        return self.player



class Player(object):
    #angle measurements are in radians
    angle = 0
    FOV = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y