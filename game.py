import pygame
import sys
from world import *
from timer import *
from raycaster import *


class Game():
    screenX = 854
    screenY = 480
    screenRatio = 1
    frameRate = 0
    lastPhysics = 0
    KEY_Q = False
    KEY_E = False
    KEY_W = False
    def __init__(self):
        self.lastFrame = timeInMillis()
        self.world = World("world.png", self.screenX, self.screenY)
        self.caster = RayCaster(self.world)
        self.loop = Timer(self.tick)
        self.screen = configureScreen(self.screenX, self.screenY)

    def start(self):
        self.loop.start()

    def tick(self):
        self.caster.cast()
        self.draw()
        self.frameRate = 1000/(timeInMillis()-self.lastFrame)
        self.lastFrame = timeInMillis()
        self.eventCatcher()

        #making physics (movement) not tied to framerate
        #*cough* looking at you Bethesda *cough*
        if(timeInMillis() - self.lastPhysics > 100):
            lastPhysics = timeInMillis()
            self.movementHandler()

    def draw(self):
        white = (255,255,255)
        red = (255,0,0)
        black = (0,0,0)
        grayish = (166, 166, 166)
        self.screen.fill(grayish)
        screenY = self.world.getScreenY()

        for i in range(0, len(self.caster.getColumnList())):
            if self.caster.getColumn(i) != None:
                columnHeight = screenY/self.caster.getColumn(i)
                pointlist = [(i, screenY/2 - columnHeight/2), (i, screenY/2 + columnHeight/2)]
                topPointlist = [(i, screenY/2 - columnHeight/2), (i, screenY/2 - columnHeight/2)]
                bottomPointlist = [(i, screenY/2 + columnHeight/2), (i, screenY/2 + columnHeight/2)]
                pygame.draw.lines(self.screen, self.caster.getColor(i), False, pointlist, 1)
                pygame.draw.lines(self.screen, black, False, topPointlist, 1)
                pygame.draw.lines(self.screen, black, False, bottomPointlist, 1)

        font = pygame.font.Font(None, 20)
        text = font.render(self.caster.getInfo(), 1, red)
        framerate = font.render("FPS: {}".format(self.frameRate), 1, red)
        self.screen.blit(text, (0, 0))
        self.screen.blit(framerate, (0, 20))

        pygame.display.update()

    def eventCatcher(self):
        #catching pygame generated events
        for event in pygame.event.get():
            #closes both the pygame module and forces the program to end
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.KEY_Q  = pygame.key.get_pressed()[pygame.K_q]
            self.KEY_E = pygame.key.get_pressed()[pygame.K_e]
            self.KEY_A = pygame.key.get_pressed()[pygame.K_a]
            self.KEY_D = pygame.key.get_pressed()[pygame.K_d]
            self.KEY_W = pygame.key.get_pressed()[pygame.K_w]
            self.KEY_S = pygame.key.get_pressed()[pygame.K_s]
            if event.type == pygame.VIDEORESIZE:
                print(event.dict['size'])
                self.world.setScreenX(event.dict['size'][0])
                self.world.setScreenY(event.dict['size'][1])
                self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)

    def movementHandler(self):
        currentAngle = self.world.getPlayer().getAngle()
        posDirX = currentAngle < math.pi/2 or currentAngle > (3/2)*math.pi
        posDirY = currentAngle > math.pi
        if(posDirX):
            xDir = 1
        else:
            xDir = -1
        if(posDirY):
            yDir = 1
        else:
            yDir = -1
        if self.KEY_Q:
            self.world.getPlayer().increaseAngle(0.1)
        elif self.KEY_E:
            self.world.getPlayer().increaseAngle(-0.1)
        if self.KEY_W:
            self.world.getPlayer().increaseX(xDir*math.fabs(math.cos(currentAngle)*0.1))
            self.world.getPlayer().increaseY(yDir*math.fabs(math.sin(currentAngle)*0.1))
        elif self.KEY_S:
            self.world.getPlayer().increaseX(-xDir*math.fabs(math.cos(currentAngle)*0.1))
            self.world.getPlayer().increaseY(-yDir*math.fabs(math.sin(currentAngle)*0.1))





def configureScreen(screenX, screenY):
    pygame.init()
    screen = pygame.display.set_mode((screenX, screenY), pygame.RESIZABLE)
    pygame.display.set_caption("PyCaster")
    return screen

def timeInMillis():
    return time.time() * 1000