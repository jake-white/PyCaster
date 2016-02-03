import sys
import random

import pygame

from world import *
from timer import *
from raycaster import *
from battle import *
from config import *


class Game():
    stepsSinceEncounter = 0
    lastFrame = 0
    frameRate = 0
    lastPhysics = 0
    actionFrame = 0
    responseFrame = 0
    KEY_LEFT = False
    KEY_RIGHT = False
    KEY_FORWARDS = False
    KEY_BACKWARDS = False
    KEY_STRAFE_LEFT = False
    KEY_STRAFE_RIGHT = False
    KEY_HEIGHTUP = False
    KEY_HEIGHTDOWN = False
    KEY_ANGLEUP = False
    KEY_ANGLEDOWN = False
    songPlaying = False
    INBATTLE = False
    BATTLESTART = False
    devtools = False
    def __init__(self):
        self.config = Config("configs/gameconfig.txt", "configs/monsterconfig.txt")
        #accessing some values from the configuration file
        self.screenX = int(self.config.getElement("screen_x"))
        self.screenY = int(self.config.getElement("screen_y"))
        self.devtools = eval(self.config.getElement("devtools"))
        self.locked_res = self.config.getElement("locked_res") == "yes"
        self.resX = self.screenX
        self.resY = self.screenY

        #defining some objects for the game to run off of
        self.world = World(self.config.getElement("worldname"), self.config, self.screenX, self.screenY)
        self.caster = RayCaster(self.world, int(self.config.getElement("light")))
        self.loop = Timer(self.tick)
        self.screen = configureScreen(self.screenX, self.screenY)
        self.nextEncounter = random.randint(int(self.config.getElement("min_encounter_steps")), int(self.config.getElement("max_encounter_steps")))
        print(int(self.config.getElement("min_encounter_steps")))
        print(self.nextEncounter)


    def start(self): #starting the game loop
        self.loop.start()

    def tick(self): #this gets called every time the game loops (ticks)
        if(not self.INBATTLE):
            if(timeInMillis() - self.lastPhysics > 500):
                lastPhysics = timeInMillis()
                self.movementHandler()

        self.eventCatcher()
        self.caster.cast()
        self.draw()
        self.frameRate = 1000/(timeInMillis()-self.lastFrame)
        self.lastFrame = timeInMillis()

        #dealing with battle encounters here
        print(self.world.getBossAlive())
        if((not self.BATTLESTART)
           and int(self.world.getPlayer().getX()) == self.world.getBossX()
           and int(self.world.getPlayer().getY()) == self.world.getBossY()
           and self.world.getBossAlive()):
            self.battle = Battle(self.world, self, "boss")
            self.BATTLESTART = True
            self.INBATTLE = True
            print("starting bossfight")
        elif(self.stepsSinceEncounter >= self.nextEncounter):
            #turning the player in direction where the battle can be displayed
            if(not self.caster.getColumn(int(self.resX/2)) == None and self.caster.getColumn(int(self.resX/2)) < 2):
                self.BATTLESTART = False
                self.world.getPlayer().increaseAngle(0.1)
            else:
                self.battle = Battle(self.world, self, "normal")
                self.BATTLESTART = True
                self.stepsSinceEncounter = 0
                self.nextEncounter = random.randint(int(self.config.getElement("min_encounter_steps")), int(self.config.getElement("max_encounter_steps")))
            self.INBATTLE = True


    def draw(self): #draws everything onscreen
        white = (255,255,255)
        red = (255,0,0)
        black = (0,0,0)
        green = (0, 255, 0)
        darkness = int(self.config.getElement("light"))*20
        screenY = self.world.getScreenY()

        #background
        for i in range(1, int(self.screenY/2)):
            intensity = darkness/(self.screenY/2) * i
            backColor = (darkness-intensity, darkness-intensity, darkness-intensity)
            pygame.draw.line(self.screen, backColor, (0, i), (self.screenX, i), 10)
            pygame.draw.line(self.screen, backColor, (0, self.screenY - i), (self.screenX, self.screenY - i), 10)

        if(self.locked_res):
            increment = self.screenX/self.resX
        else:
            increment = 1
        #drawing columns onscreen based on raycaster
        lastXValue = 0
        print(self.world.getPlayer().getCam())
        for i in range(0, len(self.caster.getColumnList())):
            lastXValue += increment
            if self.caster.getColumn(i) != None:
                columnHeight = screenY/self.caster.getColumn(i)
                if(columnHeight > screenY):
                    columnHeight = screenY
                columnX = int(lastXValue)
                columnY = int(screenY/2 - columnHeight/2) + columnHeight*self.world.getPlayer().getHeight() - 100*self.world.getPlayer().getCam()
                rectWidth = increment + 1
                rectHeight = columnHeight - int(10/(columnHeight*(1/self.world.getPlayer().getCam())))
                columnRect = pygame.Rect(columnX, columnY, rectWidth, rectHeight)
                #topRect = pygame.Rect(int(lastXValue), int(screenY/2 - columnHeight/2) - 1, increment + 1, 1)
                #bottomRect = pygame.Rect(int(lastXValue), int(screenY/2 + columnHeight/2) + 1, increment + 1, 1)
                pygame.draw.rect(self.screen, self.caster.getColor(i), columnRect, 0)
                #pygame.draw.rect(self.screen, black, topRect, 0)
                #pygame.draw.rect(self.screen, black, bottomRect, 0)


        #drawing player "hand" over the terrain
        hand_sprite = pygame.image.load(self.config.getElement("hand_sprite"))
        hand_sprite = pygame.transform.scale(hand_sprite, (int(self.screenX/3), int(self.screenX/3*(hand_sprite.get_height()/hand_sprite.get_width()))))
        self.screen.blit(hand_sprite, (self.screenX - hand_sprite.get_width(), self.screenY - hand_sprite.get_height()))

        #creating necessary fonts
        font = pygame.font.SysFont("monospace", int(self.screenX/20))
        consoleFont = pygame.font.SysFont("monospace", int(self.screenX/50))
        healthFont = pygame.font.SysFont("monospace", int(self.screenX/60))
        #drawing the battle HUD
        if(self.BATTLESTART):
            #displaying enemy
            enemy = pygame.image.load(self.battle.getMonster().getImage())
            enemy = pygame.transform.scale(enemy, (int(self.screenX/3), int((self.screenX/3)*(enemy.get_height()/enemy.get_width()))))
            self.screen.blit(enemy, (self.screenX/2 - enemy.get_width()/2, self.screenY - enemy.get_height()))
            actionList = self.battle.getActionList()
            #displaying health bars
            text_color = eval(self.config.getElement("text_color"))
            enemyHealth = healthFont.render(self.battle.getEnemyHealth(), 1, text_color)
            playerHealth = healthFont.render(self.battle.getPlayerHealth(), 1, text_color)
            healthBarWidth = int(self.screenX/10)
            healthBarHeight = int(self.screenY/30)
            pygame.draw.rect(self.screen, red, (int(self.screenX/20), int(self.screenY/3), healthBarWidth, healthBarHeight))
            pygame.draw.rect(self.screen, red, (int(self.screenX/20), int(self.screenY*(2/3)), healthBarWidth, healthBarHeight))
            pygame.draw.rect(self.screen, green, (int(self.screenX/20), int(self.screenY/3),
                                                  healthBarWidth*self.battle.getEnemyPercent(), healthBarHeight))
            pygame.draw.rect(self.screen, green, (int(self.screenX/20), int(self.screenY*(2/3)),
                                                  int(healthBarWidth*self.battle.getPlayerPercent()), healthBarHeight))
            self.screen.blit(enemyHealth, (int(self.screenX/20), int(self.screenY/3) - healthBarHeight*2))
            self.screen.blit(playerHealth, (int(self.screenX/20), int(self.screenY*(2/3)) - healthBarHeight*2))

            #displaying player actions
            for i in range(0, len(self.battle.getActionList())):
                actionText = font.render(self.battle.getActionList()[i][0], 1, red)
                pygame.draw.rect(self.screen, white, (self.screenX - (int(self.screenX/20) + actionText.get_width()), actionText.get_height()*(i+1)*2, actionText.get_width(), actionText.get_height()))
                self.screen.blit(actionText, (self.screenX - (int(self.screenX/20) + actionText.get_width()), actionText.get_height()*(i+1)*2))
            if(self.battle.getActionConsole() == ""):
                self.actionFrame = 0
                self.responseFrame = 0
            else:
                if(len(self.battle.getActionConsole()) > self.actionFrame):
                    self.actionFrame += 2
                elif(len(self.battle.getResponseConsole()) > self.responseFrame):
                    self.responseFrame += 2
                else:
                    self.battle.animationFinished()
                actionText = consoleFont.render(self.battle.getActionConsole()[:self.actionFrame], 1, red)
                responseText = consoleFont.render(self.battle.getResponseConsole()[:self.responseFrame], 1, red)
                self.screen.blit(actionText, (self.screenX/2 - actionText.get_width()/2, actionText.get_height()))
                self.screen.blit(responseText, (self.screenX/2 - responseText.get_width()/2, responseText.get_height() + actionText.get_height()))

        #developer tools here
        if(self.devtools):
            font = pygame.font.SysFont("monospace", int(self.screenX/70))
            text = font.render(self.caster.getInfo(), 1, red)
            framerate = font.render("FPS: {}".format(self.frameRate), 1, red)
            encounter = font.render("Encounter in: {} Last encounter: {}".format(self.nextEncounter, self.stepsSinceEncounter), 1, red)
            self.screen.blit(text, (0, 0))
            self.screen.blit(framerate, (0, 20))
            self.screen.blit(encounter, (0, 40))

        #this finally draws everything to the screen
        pygame.display.update()

    def eventCatcher(self):
        #catching pygame generated events
        for event in pygame.event.get():
            #closes both the pygame module and forces the program to end
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #getting keypresses
            key = "pygame.K_" + self.config.getElement("left")
            self.KEY_LEFT  = pygame.key.get_pressed()[eval("pygame.K_" + self.config.getElement("left"))]
            self.KEY_RIGHT = pygame.key.get_pressed()[eval("pygame.K_" + self.config.getElement("right"))]
            self.KEY_STRAFE_LEFT = pygame.key.get_pressed()[eval("pygame.K_" + self.config.getElement("strafe_left"))]
            self.KEY_STRAFE_RIGHT = pygame.key.get_pressed()[eval("pygame.K_" + self.config.getElement("strafe_right"))]
            self.KEY_FORWARDS = pygame.key.get_pressed()[eval("pygame.K_" + self.config.getElement("forwards"))]
            self.KEY_BACKWARDS = pygame.key.get_pressed()[eval("pygame.K_" + self.config.getElement("backwards"))]
            if(self.devtools):
                self.KEY_HEIGHTUP = pygame.key.get_pressed()[pygame.K_z];
                self.KEY_HEIGHTDOWN = pygame.key.get_pressed()[pygame.K_x];
                self.KEY_ANGLEUP = pygame.key.get_pressed()[pygame.K_r];
                self.KEY_ANGLEDOWN = pygame.key.get_pressed()[pygame.K_f];

            #resizing the window
            if event.type == pygame.VIDEORESIZE:
                self.world.setScreenX(event.dict['size'][0])
                self.world.setScreenY(event.dict['size'][1])
                self.screenX = event.dict['size'][0]
                self.screenY = event.dict['size'][1]
                self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)

            #calling battle actions based on keypresses
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

        #checking each key and doing calculations to move/turn in a direction
        if self.KEY_LEFT:
            self.world.getPlayer().increaseAngle(0.1)
        elif self.KEY_RIGHT:
            self.world.getPlayer().increaseAngle(-0.1)
        if self.KEY_FORWARDS:
            self.world.getPlayer().increaseX(xDir*math.fabs(math.cos(currentAngle)*0.1))
            self.world.getPlayer().increaseY(yDir*math.fabs(math.sin(currentAngle)*0.1))
            self.world.getPlayer().collisionCorrection()
            self.stepsSinceEncounter += 1
        elif self.KEY_BACKWARDS:
            self.world.getPlayer().increaseX(-xDir*math.fabs(math.cos(currentAngle)*0.1))
            self.world.getPlayer().increaseY(-yDir*math.fabs(math.sin(currentAngle)*0.1))
            self.world.getPlayer().collisionCorrection()
            self.stepsSinceEncounter += 1
        if self.KEY_HEIGHTUP:
            self.world.getPlayer().increaseHeight();
        elif self.KEY_HEIGHTDOWN:
            self.world.getPlayer().decreaseHeight();
        if self.KEY_ANGLEUP:
            self.world.getPlayer().increaseCam();
        elif self.KEY_ANGLEDOWN:
            self.world.getPlayer().decreaseCam();
        currentAngle -= math.pi/2
        currentAngle = validateAngle(currentAngle)
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
        if self.KEY_STRAFE_LEFT:
            self.world.getPlayer().increaseX(-xDir * math.fabs(math.cos(currentAngle)*0.1))
            self.world.getPlayer().increaseY(-yDir * math.fabs(math.sin(currentAngle)*0.1))
            self.world.getPlayer().collisionCorrection()
            self.stepsSinceEncounter += 1
        if self.KEY_STRAFE_RIGHT:
            self.world.getPlayer().increaseX(xDir * math.fabs(math.cos(currentAngle)*0.1))
            self.world.getPlayer().increaseY(yDir * math.fabs(math.sin(currentAngle)*0.1))
            self.world.getPlayer().collisionCorrection()
            self.stepsSinceEncounter += 1

    def stop(self):
        pygame.quit()
        sys.exit()

    def clearAnimation(self):
        self.actionFrame = 0
        self.responseFrame = 0



def configureScreen(screenX, screenY):
    #this creates and returns a pygame screen
    pygame.init()
    screen = pygame.display.set_mode((screenX, screenY), pygame.RESIZABLE)
    pygame.display.set_caption("PyCaster")
    return screen

def timeInMillis():
    #returns the current time in milliseconds
    return time.time() * 1000

def validateAngle(angle):
    #ensures the current angle is between 0 and 2pi
    while angle >= 2*math.pi:
        angle -= 2*math.pi
    while angle < 0:
        angle += 2*math.pi
    return angle