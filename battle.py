import pygame

class Monster():
    def __init__(self, filename, stats):
        self.stats = stats #(name, hp, attack, type)
        self.filename = filename

    def getImage(self):
        return self.filename

    def getName(self):
        return self.stats[0]

    def getHP(self):
        return self.stats[1]

    def getAttack(self):
        return self.stats[2]

    def getType(self):
        return self.stats[3]

class Battle():
    songPlaying = False
    def __init__(self, player, game):
        self.actionList = [["Wave Torch", self.torch], ["Flee", self.flee]]
        self.currentMonster = Monster("res/mettatonEX.gif", ("Mettaton", 25, 5, "random"))
        self.player = player
        self.game = game
        if(not self.songPlaying):
            self.songPlaying = True
            self.playSong()

    def getMonster(self):
        return self.currentMonster

    def end(self):
        self.game.BATTLESTART = False
        self.game.INBATTLE = False
        self.stopSong()

    def action(self, actionNumber):
        self.console = ""
        self.actionList[actionNumber][1]()

    def playSong(self):
        print("Playing undertale music.")
        pygame.mixer.music.load('res/undertale.mp3')
        pygame.mixer.music.play(-1)

    def stopSong(self):
        pygame.mixer.music.stop()

    def getActionList(self):
        return self.actionList

    def torch(self):
        self.console.join("You wave the torch at {}.".format(self.currentMonster.getName()))

    def flee(self):
        if(self.currentMonster.getType() != "boss"):
            self.end()