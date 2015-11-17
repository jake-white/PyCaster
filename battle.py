class Monster():
    def __init__(self, filename, stats):
        self.stats = stats #(hp, attack)
        self.filename = filename
    def getImage(self):
        return self.filename