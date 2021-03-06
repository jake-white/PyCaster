import math
import pygame


class World(object): #this contains information about the world (map, screen size, etc)
    bossAlive = True
    def __init__(self, worldname, config, screenX, screenY):
        print("creating new world")
        object.__init__(self)
        self.screenX = screenX
        self.screenY = screenY
        self.resX = screenX
        self.resY = screenY
        self.config = config
        self.locked_res = self.config.getElement("locked_res") == "yes"
        print(worldname)
        self.readImage(worldname)


    def readImage(self, worldname):
        self.image = pygame.image.load(worldname)
        print("size = {}".format(self.image.get_size()))
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        self.coordList = [[(255, 255, 255, 255) for _ in range(self.height)] for _ in range(self.width)]
        self.coordHeight = [[1 for _ in range(self.height)] for _ in range(self.width)]
        print("{} is {}x{}".format(worldname, self.width, self.height))
        playerX = None
        playerY = None
        bossX = None
        bossY = None

        #iterating through the image and storing every pixel by color
        for x in range (0, self.width):
            for y in range(0, self.height):
                if self.image.get_at((x, y)) == (255, 0, 0, 255) and playerX == None:
                    #this is the player spawn point
                    playerX = x
                    playerY = y
                    print(playerX)
                    print(playerY)
                    self.coordList[x][y] = (255, 255, 255) #there is not actually a red block there, rather it's blank
                elif self.image.get_at((x, y)) == (0, 255, 0, 255) and bossX == None:
                    #this is the boss spawn point
                    self.bossX = x
                    self.bossY = y
                    self.coordList[x][y] = (255, 255, 255) #there is not actually a green block there, rather it's blank
                else:
                    self.coordList[x][y] = (self.image.get_at((x, y))[0], self.image.get_at((x, y))[1], self.image.get_at((x, y))[2])

        self.player = Player(self.config, self, playerX, playerY)
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
        if(not self.locked_res):
            self.resX = self.screenX

    def setScreenY(self, screenY):
        self.screenY = screenY
        if(not self.locked_res):
            self.resY = self.screenY

    def getScreenX(self):
        return self.screenX

    def getScreenY(self):
        return self.screenY

    def getResX(self):
        return self.resX

    def getResY(self):
        return self.resY

    def getBossX(self):
        return self.bossX

    def getBossY(self):
        return self.bossY

    def killBoss(self):
        self.bossAlive = False

    def getBossAlive(self):
        return self.bossAlive


class Player(object):
    #angle measurements are in radians
    angle = 0
    FOV = math.pi/2
    maxhp = 25
    attack = 5

    def __init__(self, config, world, x, y):
        self.x = x
        self.y = y
        self.world = world
        self.config = config
        self.hp = self.maxhp
        self.angle = eval(self.config.getElement("angle"))
        self.FOV = eval(self.config.getElement("FOV"))
        self.hp = int(self.config.getElement("HP"))
        self.height = 0
        self.cam = 1;

    def collisionCorrection(self):
        if((self.world.getCoordAt(self.x, self.y) != (255, 255, 255) and self.world.getCoordAt(self.x, self.y) != (255, 0, 0)) or
                   self.x > self.world.getMaxWidth() or self.y > self.world.getMaxHeight() or self.x < 0 or self.y < 0):
            self.x = self.lastX
            self.y = self.lastY


    def getX(self):
        return self.x


    def getHeight(self):
        return self.height;

    def increaseHeight(self):
        self.height+=0.1;

    def decreaseHeight(self):
        self.height-=0.1;


    def getCam(self):
        return self.cam;

    def increaseCam(self):
        self.cam+=0.1;

    def decreaseCam(self):
        self.cam-=0.1;

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
        self.lastX = self.x
        self.x += increment

    def increaseY(self, increment):
        self.lastY = self.y
        self.y += increment

    def getFOV(self):
        return self.FOV

    def getAttack(self):
        return self.attack

    def damage(self, dmg):
        self.hp -= dmg
        if(self.hp < 0):
            self.hp = 0

    def getHP(self):
        return self.hp

    def getMaxHP(self):
        return self.maxhp

    def getAlive(self):
        return self.hp > 0