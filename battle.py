import pygame, time, random

class Monster(): #All enemy data is stored in a Monster object
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

    def getType(self): #what 'type' of monster it is (normal encounter or boss)
        return self.type

    def damage(self, dmg):
        self.hp -= dmg
        if(self.hp < 0):
            self.hp = 0

class Battle(): #Created when a battle starts
    songPlaying = False
    actionConsole = ""
    responseConsole = ""
    lastAction = 0
    animationInProgress = False
    def __init__(self, world, game, type):
        self.game = game
        self.world = world
        self.player = world.getPlayer()
        self.actionList = [[self.game.config.getElement("action1"), self.attack], [self.game.config.getElement("action2"), self.flee]]
        if(type == "normal"): #normal random encounter
            monsterList = self.game.config.getMonsterList()
            randomNum = random.randint(0, len(monsterList) - 1)
            monsterData = monsterList[randomNum]
            self.currentMonster = Monster(monsterData[0], monsterData[1], monsterData[2])
        elif(type == "boss"): #fighting the boss
            monsterData = self.game.config.getBoss()
            self.currentMonster = Monster(monsterData[0], monsterData[1], monsterData[2])
        if(not self.songPlaying): #start up battle music
            self.songPlaying = True
            self.playSong()

    def getMonster(self):
        return self.currentMonster

    def end(self):
        self.game.BATTLESTART = False
        self.game.INBATTLE = False
        self.stopSong()

    def action(self, actionNumber): #player action triggered by game key bindings
        if(not self.animationInProgress):
                self.animationInProgress = True
                self.actionConsole = ""
                self.responseConsole = ""
                self.game.clearAnimation()
                self.actionList[actionNumber][1]()

    def playSong(self):
        if(self.currentMonster.getType() == "boss"): #what music to choose
            pygame.mixer.music.load(self.game.config.getElement("boss_music"))
        else:
            pygame.mixer.music.load(self.game.config.getElement("battle_music"))
        pygame.mixer.music.play(-1)

    def stopSong(self):
        pygame.mixer.music.stop()

    def getActionList(self): #returns a list of possible actions
        return self.actionList

    def attack(self): #first action
        damage = self.player.getAttack()
        self.currentMonster.damage(damage)
        self.actionConsole = self.actionConsole + (self.game.config.getElement("action1Message").format(self.currentMonster.getName(), damage))
        if(self.currentMonster.getAlive()):
            self.actionConsole = self.actionConsole + (".")
        else:
            self.actionConsole = self.actionConsole + (", killing it.")
            if(self.currentMonster.getType() == "boss"):
                self.world.killBoss()
        if(self.currentMonster.getAlive()):
            monsterDamage = self.currentMonster.getAttack()
            self.player.damage(monsterDamage)
            self.responseConsole = self.responseConsole + ("The enemy deals {} damage in return".format(monsterDamage))
            if(self.player.getAlive()):
                self.responseConsole = self.responseConsole + (".")
            else:
                self.responseConsole = self.responseConsole + (", killing you.")

        #using a different channel so both sounds can play simultaneously
        hit = pygame.mixer.Sound(self.game.config.getElement("hit_sound"))
        pygame.mixer.find_channel().queue(hit)


    def flee(self): #second action
        if(self.currentMonster.getType() == "boss"):
            self.actionConsole = self.actionConsole = self.actionConsole + self.game.config.getElement("bossFleeMessage")
        else:
            self.end()
        animationInProgress = False

    def getActionConsole(self): #returns the first line of text output after an action
        return self.actionConsole

    def getResponseConsole(self): #returns the second line of text output after an action
        return self.responseConsole

    def animationFinished(self): #this exists to let the battle know that another action can be executed
        self.animationInProgress = False
        if(not self.player.getAlive()):
            #kills the entire program, essentially
            self.game.stop()
        elif(not self.currentMonster.getAlive()):
            #ends the battle itself
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