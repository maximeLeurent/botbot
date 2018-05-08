from .InventoryManager import InventoryManager

class PersoProcessor():
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.inventoryManager = InventoryManager()

        self.players = []

    def startPlayer(self, players):
        self.players = players

    def getPrices(self, listIng):
        print("GetPrices %s"%str(listIng))

    def newOrder(self, order):
        bestAffinity = 0
        bestPlayer = None
        for player in self.players:
            if bestAffinity < player.orderAffinity():
                pass
