from battle import Monster

class Config():
    elements = list()
    monsters = list()
    boss = None
    def __init__(self, configFile, monsterConfigFile):
        #initializes the object with 2 config file paths

        #first, looking through the game settings and saving them
        self.worldfile = open(configFile, 'r')
        num_lines = sum(1 for line in open(configFile, 'r'))
        for i in range(0, num_lines):
            currentLine = self.worldfile.readline().strip()
            if(currentLine.find('#') == -1 and currentLine != "\n" and currentLine != ""):
                #this indicates a comment in the config file
                if(currentLine.find("=") != -1):
                    #if it's formatted correctly with '=' then save it
                    element = currentLine.split("=")[0]
                    value = currentLine.split("=")[1]
                    self.elements.append([element, value])


        #now looking through the monsters and saving them
        self.monsterFile = open(monsterConfigFile, 'r')
        num_lines = sum(1 for line in open(monsterConfigFile, 'r'))
        for i in range(0, num_lines):
            currentLine = self.monsterFile.readline().strip()
            if(currentLine.find('#') == -1 and currentLine != "\n" and currentLine != ""):
                monster = eval(currentLine)
                if(monster[2] == "normal"):
                    self.monsters.append(monster)
                elif(monster[2] == "boss"):
                    self.boss = monster

    def getElement(self, element):
        #returns the value of a given element
        for i in range(0, len(self.elements)):
            if self.elements[i][0] == element:
                return self.elements[i][1]
        return None

    def getMonsterList(self):
        return self.monsters

    def getBoss(self):
        #returns the boss information
        return self.boss