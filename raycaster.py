import math


class RayCaster(object):
    def __init__(self, world, screenX):
        self.world = world
        self.screenX = screenX
        #columns of the screen
        #value = distance, None = nothing there
        self.columns = [None] * self.getScreenX()


    def cast(self):
        angleIncrement = self.getPlayer().getFOV()/self.screenX
        startingAngle = self.getPlayer().getAngle() - self.getPlayer().getFOV()/2
        endingAngle = self.getPlayer().getAngle() + self.getPlayer().getFOV()/2
        currentAngle = startingAngle
        playerX = self.getPlayer().getX()
        playerY = self.getPlayer().getY()
        for i in range(0, self.screenX):
            currentAngle = validateAngle(currentAngle)
            posDirX = currentAngle < math.pi/2 or currentAngle > (3/2)*math.pi
            posDirY = currentAngle > math.pi
            #checking horizontally
            if(posDirY):
                startY = int(playerY) + 1
            else:
                startY = int(playerY)
            currentAngle += angleIncrement


    def getColumn(self, col):
        return self.columns[col]

    def getColumnList(self):
        return self.columns

    def getPlayer(self):
        return self.world.getPlayer()

    def getScreenX(self):
        return self.screenX

    def getWorld(self):
        return self.world

def validateAngle(angle):
    while angle >= 2*math.pi:
        angle -= 2*math.pi
    while angle < 0:
        angle += 2*math.pi
    return angle