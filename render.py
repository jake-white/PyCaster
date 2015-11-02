import pygame, sys


class Screen():
    def __init__(self, raycaster, title, width, height):
        self.width = width
        self.height = height
        self.title = title
        self.raycaster = raycaster
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
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