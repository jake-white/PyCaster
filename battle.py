import pygame

class Monster():
    def __init__(self, filename, stats, type):
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
    console = ""
    def __init__(self, player, game):
        self.actionList = [["Attack", self.attack], ["Flee", self.flee]]
        self.currentMonster = Monster("res/mettatonEX.gif", ("Mettaton", 25, 5, "random"), "normal")
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
        if(self.currentMonster.getType() == "boss"):
            pygame.mixer.music.load(self.game.config.getElement("boss_music"))
        else:
            pygame.mixer.music.load(self.game.config.getElement("battle_music"))
        pygame.mixer.music.play(-1)

    def stopSong(self):
        pygame.mixer.music.stop()

    def getActionList(self):
        return self.actionList

    def attack(self):
        print("attacking")
        self.console = self.console.join("You wave the torch at {}.".format(self.currentMonster.getName()), "\n")
        self.console = self.console.join("The fires burns the foe and deals {} damage.".format(self.player.getAttack()), "\n")
        print(self.console)


    def flee(self):
        if(self.currentMonster.getType() != "boss"):
            self.end()

    def getConsole(self):
        return self.console