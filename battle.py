import pygame, time, random

class Monster():
    def __init__(self, filename, stats, type):
        self.stats = stats #(name, hp, attack)
        self.filename = filename
        self.type = type
        self.name = self.stats[0]
        self.maxhp = self.stats[1]
        self.hp = self.maxhp
        self.attack = stats[2]

    def getImage(self):
        return self.filename

    def getName(self):
        return self.name

    def getHP(self):
        return self.hp

    def getMaxHP(self):
        return self.maxhp

    def getAlive(self):
        return self.hp > 0

    def getAttack(self):
        return self.attack

    def getType(self):
        return self.type

    def damage(self, dmg):
        self.hp -= dmg
        if(self.hp < 0):
            self.hp = 0

class Battle():
    songPlaying = False
    actionConsole = ""
    responseConsole = ""
    lastAction = 0
    animationInProgress = False
    def __init__(self, player, game, type):
        self.game = game
        self.player = player
        self.actionList = [[self.game.config.getElement("action1"), self.attack], [self.game.config.getElement("action2"), self.flee]]
        if(type == "normal"):
            monsterList = self.game.config.getMonsterList()
            randomNum = random.randint(0, len(monsterList) - 1)
            monsterData = monsterList[randomNum]
            self.currentMonster = Monster(monsterData[0], monsterData[1], monsterData[2])
        elif(type == "boss"):
            monsterData = self.game.config.getBoss()
            self.currentMonster = Monster(monsterData[0], monsterData[1], monsterData[2])
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
        if(not self.checkEndCondition() and not self.animationInProgress):
                self.animationInProgress = True
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


    def flee(self):
        if(self.currentMonster.getType() != "boss"):
            self.end()

    def getActionConsole(self):
        return self.actionConsole

    def getResponseConsole(self):
        return self.responseConsole

    def checkEndCondition(self):
        #if the battle should end this will return True
        return not self.currentMonster.getAlive() or not self.player.getAlive()

    def animationFinished(self):
        self.animationInProgress = False
        if(self.checkEndCondition()):
            self.end()

    def getEnemyHealth(self):
        return "{}: {}/{}".format(self.currentMonster.getName(), self.currentMonster.getHP(), self.currentMonster.getMaxHP())

    def getPlayerHealth(self):
        return "You: {}/{}".format(self.player.getHP(), self.player.getMaxHP())

    def getEnemyPercent(self):
        return self.currentMonster.getHP()/self.currentMonster.getMaxHP()

    def getPlayerPercent(self):
        return self.player.getHP()/self.player.getMaxHP()

def timeInMillis():
    return time.time() * 1000