import pygame, sys

class Screen():
    def __init__(self, title, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((640,480))
        self.white = (255,255,255)

    def draw(self):
        print("drawn!")
        self.screen.fill(self.white)
        pygame.display.update()
        self.eventCatcher()

    def eventCatcher(self):
        #catching pygame generated events
        for event in pygame.event.get():
            #closes both the pygame module and forces the program to end
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()