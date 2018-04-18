from .InventoryManager import InventoryManager

class PersoProcessor():
    def __init__(self):
        self.inventoryManager = InventoryManager()

    def getPrices(self, listIng):
        print("GetPrices %s"%str(listIng))
