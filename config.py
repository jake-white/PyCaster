from battle import Monster

class Config():
    elements = list()
    monsters = list()
    boss = None
    def __init__(self, configFile, monsterConfigFile):
        self.worldfile = open(configFile, 'r')
        num_lines = sum(1 for line in open(configFile, 'r'))
        for i in range(0, num_lines):
            currentLine = self.worldfile.readline().strip()
            if(currentLine.find('#') == -1 and currentLine != "\n" and currentLine != ""):
                #This indicates a comment
                if(currentLine.find("=") != -1):
                    element = currentLine.split("=")[0]
                    value = currentLine.split("=")[1]
                    self.elements.append([element, value])
                    #print("Found element {}={}".format(element, value))
                else:
                    pass
                    #print("Did not find '=' within {} of {}".format(currentLine), configFile)

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
        for i in range(0, len(self.elements)):
            if self.elements[i][0] == element:
                return self.elements[i][1]
        return None

    def getMonsterList(self):
        return self.monsters

    def getBoss(self):
        return self.boss