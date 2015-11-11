import math
from geometry import *


class RayCaster(object):
    def __init__(self, world, screenX):
        self.world = world
        self.screenX = screenX
        #columns of the screen
        #value = distance, None = nothing there
        self.columns = [None] * self.getScreenX()
        self.colors = [None] * self.getScreenX()


    def cast(self):
        #defining some stuff to make this easier and not call 12 thousand functions every line
        angleIncrement = self.getPlayer().getFOV()/self.screenX
        angle = validateAngle(self.getPlayer().getAngle())
        startingAngle = angle + self.getPlayer().getFOV()/2
        endingAngle = angle - self.getPlayer().getFOV()/2
        currentAngle = startingAngle
        playerX = self.getPlayer().getX()
        playerY = self.getPlayer().getY()
        playerPoint = Point(playerX, playerY)
        #starting casting rays for every pixel of screen length
        for i in range(0, self.screenX):
            currentAngle = validateAngle(currentAngle)
            posDirX = currentAngle < math.pi/2 or currentAngle > (3/2)*math.pi
            posDirY = currentAngle > math.pi

            #------------checking horizontally------------
            if(posDirY):
                startY = int(playerY) + 1
                deltaY = 1
            else:
                startY = int(playerY)
                deltaY = -1
            distFromPlayerY = math.fabs(startY - playerY)
            distFromPlayerX = math.fabs((distFromPlayerY/math.tan(currentAngle)))
            if(posDirX):
                startX = playerX + distFromPlayerX
                deltaX = math.fabs(deltaY/math.tan(currentAngle))
            else:
                startX = playerX - distFromPlayerX
                deltaX = -math.fabs(deltaY/math.tan(currentAngle))

            hit = False
            currentPoint = Point(startX, startY)
            while not hit:
                if(posDirY):
                    checkPoint = Point(currentPoint.x, currentPoint.y)
                else:
                    checkPoint = Point(currentPoint.x, currentPoint.y - 1)
                if currentPoint.x > self.world.getMaxWidth() or currentPoint.y > self.world.getMaxHeight() or currentPoint.x < 0 or currentPoint.y < 0:
                    distanceX = -1
                    hit = True
                elif self.world.getCoordAt(checkPoint) != 0:
                    print("Horizontal block at {}".format(checkPoint.toString()))
                    hit = True
                    distanceX = playerPoint.distanceTo(currentPoint)

                currentPoint.increaseX(deltaX)
                currentPoint.increaseY(deltaY)

            #------------checking vertically------------
            if(posDirX):
                startX = int(playerX) + 1
                deltaX = 1
            else:
                startX = int(playerX)
                deltaX = -1
            distFromPlayerX = math.fabs(startX - playerX)
            distFromPlayerY = math.fabs(distFromPlayerX*math.tan(currentAngle))
            if(posDirY):
                startY = playerY + distFromPlayerY
                deltaY = math.fabs(math.tan(currentAngle)*(deltaX))
            else:
                startY = playerY - distFromPlayerY
                deltaY = -math.fabs(math.tan(currentAngle)*(deltaX))

            hit = False
            currentPoint = Point(startX, startY)
            while not hit:
                if posDirX:
                    checkPoint = Point(currentPoint.x, currentPoint.y)
                else:
                    checkPoint = Point(currentPoint.x - 1, currentPoint.y)
                if currentPoint.x > self.world.getMaxWidth() or currentPoint.y > self.world.getMaxHeight() or currentPoint.x < 0 or currentPoint.y < 0:
                    distanceY = -1
                    hit = True
                elif self.world.getCoordAt(checkPoint) != 0:
                    print("Vertical block at {}".format(checkPoint.toString()))
                    hit = True
                    distanceY = playerPoint.distanceTo(currentPoint)

                currentPoint.increaseX(deltaX)
                currentPoint.increaseY(deltaY)

            if((distanceX <= distanceY or distanceY < 0) and distanceX >= 0):
                self.columns[i] = distanceX
                self.colors[i] = (0, 255, 0)
            elif distanceY >= 0:
                self.columns[i] = distanceY
                self.colors[i] = (0,0,0)
            else:
                self.columns[i] = -1
                self.colors[i] = (0,0,0)
            if(self.columns[i] == 0):
                #don't wanna divide by zero
                self.columns[i] = 0.1
            currentAngle -= angleIncrement
            self.info = "Player: ({}, {}) at A = {}".format(playerX, playerY, angle)


    def getColumn(self, col):
        return self.columns[col]

    def getColor(self, col):
        return self.colors[col]

    def getColumnList(self):
        return self.columns

    def getPlayer(self):
        return self.world.getPlayer()

    def getScreenX(self):
        return self.screenX

    def getWorld(self):
        return self.world

    def getInfo(self):
        return self.info


def validateAngle(angle):
    while angle >= 2*math.pi:
        angle -= 2*math.pi
    while angle < 0:
        angle += 2*math.pi
    return angle

def getQuadrant(angle):
    if angle < (1/2)*math.pi:
        return 1
    elif angle < math.pi:
        return 2
    elif angle < (3/2)*math.pi:
        return 3
    elif angle < 2*math.pi:
        return 4