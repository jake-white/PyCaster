class RayCaster(object):
    def __init__(self, world, screenX):
        self.world = world
        self.screenX = screenX
    def cast(self):
        self.columns = [None] * self.getScreenX()
    def getColumn(self, col):
        return self.columns[col]
    def getPlayer(self):
        return self.player
    def getScreenX(self):
        return self.screenX
    def getWorld(self):
        return self.world