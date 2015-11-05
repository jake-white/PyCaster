import pygame
import sys
from world import *
from timer import *
from raycaster import *


class Game():
    screenX = 400
    screenY = 300
    def __init__(self):
        world = World(5, 5, 2, 2)
        self.caster = RayCaster(world, self.screenX)
        self.loop = Timer(self.tick)
        self.screen = configureScreen(self.screenX, self.screenY)
        print("Player placed at {}, {} in a {}x{} world.".format(world.getPlayer().getX(), world.getPlayer().getY(), world.getLength(), world.getWidth()))
        print(world.getCoords())

    def start(self):
        self.loop.start()

    def tick(self):
        self.caster.cast()
        self.draw()
        print("TICK")

    def draw(self):
        print("drawn!")
        white = (255,255,255)
        self.screen.fill(white)
        pygame.display.update()
        self.eventCatcher()

    def eventCatcher(self):
        #catching pygame generated events
        for event in pygame.event.get():
            #closes both the pygame module and forces the program to end
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

def configureScreen(screenX, screenY):
        pygame.init()
        screen = pygame.display.set_mode((screenX, screenY))
        pygame.display.set_caption("PyCaster")
        return screen