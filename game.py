import pygame
import sys
from world import *
from timer import *
from raycaster import *


class Game():
    screenX = 400
    screenY = 300
    def __init__(self):
        self.world = World(5, 5, 1, 1)
        self.caster = RayCaster(self.world, self.screenX)
        self.loop = Timer(self.tick)
        self.screen = configureScreen(self.screenX, self.screenY)
        print(self.world.getCoords())

    def start(self):
        self.loop.start()

    def tick(self):
        self.caster.cast()
        self.draw()
        self.eventCatcher()

    def draw(self):
        white = (255,255,255)
        red = (255,0,0)
        black = (0,0,0)
        self.screen.fill(white)
        pygame.draw.lines(self.screen, red, False, [(self.screenX/2, 0), (self.screenX/2, self.screenY)], 1)

        for i in range(0, len(self.caster.getColumnList())):
            if(self.caster.getColumn(i) >= 0):
                columnHeight = self.screenY/self.caster.getColumn(i)
                pointlist = [(i, self.screenY/2 - columnHeight/2), (i, self.screenY/2 + columnHeight/2)]
                pygame.draw.lines(self.screen, self.caster.getColor(i), False, pointlist, 1)

        font = pygame.font.Font(None, 20)
        text = font.render(self.caster.getInfo(), 1, red)
        textpos = text.get_rect()
        self.screen.blit(text, textpos)

        pygame.display.update()

    def eventCatcher(self):
        #catching pygame generated events
        for event in pygame.event.get():
            #closes both the pygame module and forces the program to end
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_q]:
                    self.world.getPlayer().increaseAngle(0.1)
                if pygame.key.get_pressed()[pygame.K_e]:
                    self.world.getPlayer().increaseAngle(-0.1)
                if pygame.key.get_pressed()[pygame.K_a]:
                    self.world.getPlayer().increaseX(-0.1)
                if pygame.key.get_pressed()[pygame.K_d]:
                    self.world.getPlayer().increaseX(0.1)
                if pygame.key.get_pressed()[pygame.K_w]:
                    self.world.getPlayer().increaseY(-0.1)
                if pygame.key.get_pressed()[pygame.K_s]:
                    self.world.getPlayer().increaseY(0.1)

def configureScreen(screenX, screenY):
        pygame.init()
        screen = pygame.display.set_mode((screenX, screenY))
        pygame.display.set_caption("PyCaster")
        return screen