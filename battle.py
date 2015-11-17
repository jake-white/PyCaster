import pygame

class Monster():
    def __init__(self, filename, stats):
        self.stats = stats #(hp, attack)
        self.filename = filename
    def getImage(self):
        return self.filename

class Battle():
    songPlaying = False
    def __init__(self, player):
        self.actionList = [["Fight", self.fight], ["Flee", self.flee]]
        self.currentMonster = Monster("res/mettatonEX.gif", (25, 5))
        if(not self.songPlaying):
            self.songPlaying = True
            self.playSong()

    def getMonster(self):
        return self.currentMonster

    def action(self, actionNumber):
        self.actionList[actionNumber][1]()

    def playSong(self):
        pygame.mixer.music.load('res/undertale.mp3')
        pygame.mixer.music.play(-1)

    def stopSong(self):
        pygame.mixer.music.stop()

    def fight(self):
        print("Fighting")

    def flee(self):
        print("Fleeing")