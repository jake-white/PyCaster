import pygame, time

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

    def getAlive(self):
        return self.stats[1] > 0

    def getAttack(self):
        return int(self.stats[2])

    def getType(self):
        return self.stats[3]

    def damage(self, dmg):
        self.stats[1] -= dmg
        if(self.stats[1] < 0):
            self.stats[1] = 0

class Battle():
    songPlaying = False
    actionConsole = ""
    responseConsole = ""
    actionTimeLimit = 1000
    lastAction = 0
    def __init__(self, player, game):
        self.actionList = [["Attack", self.attack], ["Flee", self.flee]]
        self.currentMonster = Monster("res/mettatonEX.gif", ["Mettaton", 25, 5, "random"], "normal")
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
        if(timeInMillis() - self.lastAction > self.actionTimeLimit):
            self.actionConsole = ""
            self.responseConsole = ""
            self.game.clearAnimation()
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
        self.actionConsole = self.actionConsole + ("You wave the torch at {}. ".format(self.currentMonster.getName()))
        damage = self.player.getAttack()
        self.actionConsole = self.actionConsole + ("The fires burns the foe and deals {} damage. ".format(damage))
        self.currentMonster.damage(damage)
        if(self.currentMonster.getAlive()):
            monsterDamage = self.currentMonster.getAttack()
            self.player.damage(monsterDamage)
            self.responseConsole = self.responseConsole + ("The enemy deals {} damage in return.".format(monsterDamage))
        #using a different channel so both sounds can play simultaneously
        hit = pygame.mixer.Sound(self.game.config.getElement("hit_sound"))
        pygame.mixer.find_channel().queue(hit)
        self.checkEndCondition()



        self.lastAction = timeInMillis()


    def flee(self):
        if(self.currentMonster.getType() != "boss"):
            self.end()

    def getActionConsole(self):
        return self.actionConsole

    def getResponseConsole(self):
        return self.responseConsole

    def checkEndCondition(self):
        if(not self.currentMonster.getAlive() or not self.player.getAlive()):
            self.end()

def timeInMillis():
    return time.time() * 1000