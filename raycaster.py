import math


class RayCaster(object):
    drawDistance = 5
    def __init__(self, world, screenX):
        self.world = world
        self.screenX = screenX
        #columns of the screen
        #value = distance, None = nomath.tan there
        self.columns = [None] * self.getScreenX()
        self.colors = [None] * self.getScreenX()


    def cast(self):
        #defining some stuff to make this easier and not call 12 thousand functions every line
        angleIncrement = self.getPlayer().getFOV()/self.screenX
        angle = validateAngle(self.getPlayer().getAngle())
        startingAngle = angle + self.getPlayer().getFOV()/2
        currentAngle = startingAngle
        playerX = self.getPlayer().getX()
        playerY = self.getPlayer().getY()
        maxX = self.world.getMaxWidth()
        maxY = self.world.getMaxHeight()
        #starting casting rays for every pixel of screen length
        for i in range(0, self.screenX):
            fisheye = math.cos(math.fabs(currentAngle-angle))
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
            currentX = startX
            currentY = startY
            while not hit:
                checkX = currentX
                if(posDirY):
                    checkY = currentY
                else:
                    checkY = currentY - 1
                if currentX > maxX or currentY > maxY or currentX < 0 or currentY < 0:
                    distanceX = -1
                    hit = True
                elif self.world.getCoordAt(checkX, checkY) != (255, 255, 255):
                    hit = True
                    distanceX = self.distanceTo(playerX, playerY, currentX, currentY)*fisheye
                    if(currentX %1 < 0.05):
                        colorX = (0,0,0)
                    else:
                        colorX = self.world.getCoordAt(checkX, checkY)

                currentX += deltaX
                currentY += deltaY

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
            currentX = startX
            currentY = startY
            while not hit:
                checkY = currentY
                if posDirX:
                    checkX = currentX
                else:
                    checkX = currentX - 1
                if currentX > maxX or currentY > maxY or currentX < 0 or currentY < 0:
                    distanceY = -1
                    hit = True
                elif self.world.getCoordAt(checkX, checkY) != (255, 255, 255):
                    hit = True
                    distanceY = self.distanceTo(playerX, playerY, currentX, currentY)*fisheye
                    if(currentY %1 < 0.05):
                        colorY = (0,0,0)
                    else:
                        colorY = self.world.getCoordAt(checkX, checkY)

                currentX += deltaX
                currentY += deltaY

            if((distanceX <= distanceY or distanceY < 0) and distanceX >= 0):
                self.columns[i] = distanceX
                self.colors[i] = colorX
            elif distanceY >= 0:
                self.columns[i] = distanceY
                self.colors[i] = colorY
            else:
                self.columns[i] = None
                self.colors[i] = (255, 255, 255)
            if(self.columns[i] == 0):
                #don't wanna divide by zero
                self.columns[i] = 0.1
            currentAngle -= angleIncrement
            self.info = "Player: ({}, {}) at A = {}".format(playerX, playerY, angle)

    def distanceTo(self, x1, y1, x2, y2):
        #d^2 = x^2 + y^2
        return math.sqrt(math.pow(y1 - y2, 2) + math.pow(x1 - x2, 2))


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