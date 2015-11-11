import math
from geometry import *


class World(object):
    coordList = list()

    def __init__(self, width, height, playerX, playerY):
        object.__init__(self)
        #self.coordList = [[0 for _ in range(length)] for _ in range(width)]
        self.coordList = [[0,0,1,0,0],
                          [0,0,0,0,0],
                          [0,0,1,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,0]]
        self.width = width
        self.height = height
        self.player = Player(playerX, playerY)

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

    def getCoordAt(self, point):
        #x and y are reversed because the list is visually "reversed" from the coordinate plane.
        #I could make it proper but that would just mess with my ability to debug.
        return self.coordList[int(point.getY())][int(point.getX())]

    def getPlayer(self):
        return self.player


class Player(object):
    #angle measurements are in radians
    angle = 0
    FOV = math.pi/2

    def __init__(self, x, y):
        self.point = Point(x, y)

    def getX(self):
        return self.point.getX()

    def getY(self):
        return self.point.getY()

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
        self.point.increaseX(increment)

    def increaseY(self, increment):
        self.point.increaseY(increment)

    def getFOV(self):
        return self.FOV
