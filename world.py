import math
from PIL import Image


class World(object):

    def __init__(self, worldname, screenX, screenY):
        object.__init__(self)
        self.screenX = screenX
        self.screenY = screenY
        self.readImage(worldname)


    def readImage(self, worldname):
        self.image = Image.open(worldname).convert('RGB')
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.coordList = [[(0, 0, 0) for _ in range(self.height)] for _ in range(self.width)]
        print("world.png is {}x{}".format(self.width, self.height))
        playerX = None
        playerY = None
        for x in range (0, self.width):
            for y in range(0, self.height):
                if self.image.getpixel((x, y)) == (255, 0, 0) and playerX == None:
                    playerX = x
                    playerY = y
                    self.coordList[x][y] = (255, 255, 255) #there is not actually a red block there, rather it's blank
                else:
                    self.coordList[x][y] = self.image.getpixel((x, y))
                    if(self.coordList[x][y] != (255, 255, 255)):
                        print("Point confirmed at ({}, {})".format(x, y))

        self.player = Player(playerX, playerY)
        print("Player created at ({}, {})".format(playerX, playerY))


    def getWidth(self):
        return self.width

    def getMaxWidth(self):
        return self.width - 1

    def getMaxHeight(self):
        return self.height - 1

    def getHeight(self):
        return self.height

    def getCoords(self):
        return self.coordList

    def getCoordAt(self, x, y):
        #x and y are reversed because the list is visually "reversed" from the coordinate plane.
        #I could make it proper but that would just mess with my ability to debug.
        return self.coordList[int(x)][int(y)]

    def getPlayer(self):
        return self.player

    def setScreenX(self, screenX):
        self.screenX = screenX

    def setScreenY(self, screenY):
        self.screenY = screenY

    def getScreenX(self):
        return self.screenX

    def getScreenY(self):
        return self.screenY


class Player(object):
    #angle measurements are in radians
    angle = math.pi/3
    FOV = math.pi/2

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getAngle(self):
        self.validateAngle()
        return self.angle

    def validateAngle(self):
        #ensures the current angle is between 0 and 2pi
        while self.angle >= 2*math.pi:
            self.angle -= 2*math.pi
        while self.angle < 0:
            self.angle += 2*math.pi

    def increaseAngle(self, increment):
        self.angle += increment
        self.validateAngle()

    def increaseX(self, increment):
        self.x += increment

    def increaseY(self, increment):
        self.y += increment

    def getFOV(self):
        return self.FOV
