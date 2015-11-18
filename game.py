import pygame
import sys
import random
from world import *
from timer import *
from raycaster import *
from battle import *


class Game():
    originalscreenX = 854
    originalscreenY = 480
    screenX = 854
    screenY = 480
    screenRatio = 1
    frameRate = 0
    lastPhysics = 0
    KEY_Q = False
    KEY_E = False
    KEY_W = False
    KEY_S = False
    songPlaying = False
    INBATTLE = False
    BATTLESTART = False
    def __init__(self):
        self.lastFrame = timeInMillis()
        self.world = World("res/world.png", self.screenX, self.screenY)
        self.caster = RayCaster(self.world)
        self.loop = Timer(self.tick)
        self.screen = configureScreen(self.screenX, self.screenY)
        self.nextEncounter = random.randint(0, 100)
        self.stepsSinceEncounter = 0

    def start(self): #starting the game loop
        self.loop.start()

    def tick(self): #this gets called every time the game loops (ticks)
        if(not self.INBATTLE):
            if(timeInMillis() - self.lastPhysics > 100):
                lastPhysics = timeInMillis()
                self.movementHandler()

        self.eventCatcher()
        self.caster.cast()
        self.draw()
        self.frameRate = 1000/(timeInMillis()-self.lastFrame)
        self.lastFrame = timeInMillis()
        if(self.stepsSinceEncounter >= self.nextEncounter):
            if(self.caster.getColumn(int(self.screenX/2)) < 2):
                self.BATTLESTART = False
                self.world.getPlayer().increaseAngle(0.1)
            else:
                self.battle = Battle(self.world.getPlayer(), self)
                self.BATTLESTART = True
                self.stepsSinceEncounter = 0
                self.nextEncounter = random.randint(0, 100)
            self.INBATTLE = True

        #making physics (movement) not tied to framerate
        #*cough* looking at you Bethesda *cough*


    def draw(self): #draws everything onscreen
        white = (255,255,255)
        red = (255,0,0)
        black = (0,0,0)
        darkness = 100
        screenY = self.world.getScreenY()

        #background
        for i in range(1, int(self.screenY/2)):
            intensity = darkness/(self.screenY/2) * i
            backColor = (darkness-intensity, darkness-intensity, darkness-intensity)
            print(backColor)
            pygame.draw.line(self.screen, backColor, (0, i), (self.screenX, i), 10)
            pygame.draw.line(self.screen, backColor, (0, self.screenY - i), (self.screenX, self.screenY - i), 10)

        for i in range(0, len(self.caster.getColumnList())):
            if self.caster.getColumn(i) != None:
                columnHeight = screenY/self.caster.getColumn(i)
                pointlist = [(i, screenY/2 - columnHeight/2), (i, screenY/2 + columnHeight/2)]
                topPointlist = [(i, screenY/2 - columnHeight/2), (i, screenY/2 - columnHeight/2)]
                bottomPointlist = [(i, screenY/2 + columnHeight/2), (i, screenY/2 + columnHeight/2)]
                pygame.draw.lines(self.screen, self.caster.getColor(i), False, pointlist, 1)
                pygame.draw.lines(self.screen, black, False, topPointlist, 1)
                pygame.draw.lines(self.screen, black, False, bottomPointlist, 1)

        torch = pygame.image.load("res/torch.png")
        self.screen.blit(torch, (self.screenX - torch.get_width(), self.screenY - torch.get_height()))

        font = pygame.font.SysFont("monospace", int(self.screenX/20))
        #battle HUD
        if(self.BATTLESTART):
            #displaying enemy
            enemy = pygame.image.load(self.battle.getMonster().getImage())
            enemy = pygame.transform.scale(enemy, (int(enemy.get_width()*self.screenX/self.originalscreenX), int(enemy.get_height()*self.screenY/self.originalscreenY)))
            self.screen.blit(enemy, (self.screenX/2 - enemy.get_width()/2, self.screenY/2))
            actionList = self.battle.getActionList()
            for i in range(0, len(self.battle.getActionList())):
                actionText = font.render(self.battle.getActionList()[i][0], 1, red)
                pygame.draw.rect(self.screen, white, (self.screenX - (20 + actionText.get_width()), actionText.get_height()*(i+1)*2, actionText.get_width(), actionText.get_height()))
                self.screen.blit(actionText, (self.screenX - (20 + actionText.get_width()), actionText.get_height()*(i+1)*2))



        #developer tools here
        font = pygame.font.SysFont("monospace", int(self.screenX/70))
        text = font.render(self.caster.getInfo(), 1, red)
        framerate = font.render("FPS: {}".format(self.frameRate), 1, red)
        encounter = font.render("Encounter in: {} Last encounter: {}".format(self.nextEncounter, self.stepsSinceEncounter), 1, red)
        self.screen.blit(text, (0, 0))
        self.screen.blit(framerate, (0, 20))
        self.screen.blit(encounter, (0, 40))

        pygame.display.update()

    def eventCatcher(self): #catches pygame events
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
                self.world.setScreenX(event.dict['size'][0])
                self.world.setScreenY(event.dict['size'][1])
                self.screenX = event.dict['size'][0]
                self.screenY = event.dict['size'][1]
                self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
            if(self.BATTLESTART):
                actionNumber = 0
                for i in range(pygame.K_1, pygame.K_4):
                    if pygame.key.get_pressed()[i]:
                        self.battle.action(actionNumber)
                    actionNumber += 1


    def movementHandler(self): #uses info from eventCatcher
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
            self.world.getPlayer().collisionCorrection()
            self.stepsSinceEncounter += 1
        elif self.KEY_S:
            self.world.getPlayer().increaseX(-xDir*math.fabs(math.cos(currentAngle)*0.1))
            self.world.getPlayer().increaseY(-yDir*math.fabs(math.sin(currentAngle)*0.1))
            self.world.getPlayer().collisionCorrection()
            self.stepsSinceEncounter += 1

def configureScreen(screenX, screenY):
    pygame.init()
    screen = pygame.display.set_mode((screenX, screenY), pygame.RESIZABLE)
    pygame.display.set_caption("PyCaster")
    return screen

def timeInMillis():
    return time.time() * 1000