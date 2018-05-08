from PyQt5 import QtCore
from PyQt5.QtCore import QVariant
from PriceToStr import priceToStr

class TablePriceIngredientModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mainWin):
        super(QtCore.QAbstractTableModel, self).__init__(parent)
        self.activeIngredient = None
        self.header =  ["Name", "Q", "To Buy", "Prix x 1", "#", "Prix x 10","#", "Prix x 100","#", "Smart Price"]
        self.columnNumber = [4,6,8]
        self.infoPrices = []
        self.nbCraft = 1
        self.mainWin = mainWin

    def majActiveIngredient(self, ingredient):
        self.activeIngredient = ingredient
        self.refresh()

    def __recalculateSmartPrice(self,n):
        self.infoPrices[n].calculateSmartPrice(self.nbCraft)

    def __recalculateSmartPriceAll(self):
        for n in range(len(self.infoPrices)):
            self.__recalculateSmartPrice(n)

    def majNbCraft(self, newNumber):
        if(self.nbCraft != newNumber):
            self.layoutAboutToBeChanged.emit()
            self.nbCraft = newNumber
            self.__recalculateSmartPriceAll()
            self.layoutChanged.emit()

    def majPrice(self,ing, price, quantite):
        for n,infoPrice in enumerate(self.infoPrices):
            if(infoPrice.ing.id_ == ing.id_):
                self.layoutAboutToBeChanged.emit()
                if(quantite == 1):
                    infoPrice.price_1 = price
                elif(quantite == 10):
                    infoPrice.price_10 = price
                elif(quantite == 100):
                    infoPrice.price_100 = price
                self.__recalculateSmartPrice(n)
                self.layoutChanged.emit()
                break

    def achatDone(self, ing,  newPrice,quant):
        for infoPrice in self.infoPrices:
            if(infoPrice.ing.id_ == ing.id_):
                infoPrice.quant_hol += quant
                self.majPrice(ing,newPrice,quant)

    def refresh(self):
        self.layoutAboutToBeChanged.emit()
        self.infoPrices = self.mainWin.dbProcessor.getCurrentPriceIngReceipt(self.activeIngredient)
        for infoPrice in self.infoPrices:
            infoPrice.setQuantInvent(self.mainWin.persoProcessor.inventoryManager.getQuantInvent(infoPrice.ing))
        self.__recalculateSmartPriceAll()
        self.layoutChanged.emit()

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QVariant(self.header[col])
        return QVariant()

    def rowCount(self, parent):
        return len(self.infoPrices)+1

    def columnCount(self,parent):
        return 10

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole and index.column() in self.columnNumber:
                self.infoPrices[index.row()].setSmartQuant((index.column()-4)/2,value)
                return True
        return False

    def flags(self, index):
        if (index.column() in self.columnNumber and index.row()< len(self.infoPrices)):
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
        if(not index.isValid()):
            return QVariant()
        if role == QtCore.Qt.DisplayRole:
            if(index.row() < len(self.infoPrices)):
                infoPrice = self.infoPrices[index.row()]
                if(index.column() == 0):
                    return QVariant(infoPrice.ing.nom)
                elif(index.column() == 1):
                    return QVariant(infoPrice.quant)
                elif(index.column() == 2):
                    return QVariant(infoPrice.quant*self.nbCraft - infoPrice.quant_hol)
                elif(index.column() == 3):
                    return QVariant(priceToStr(infoPrice.price_1))#, infoPrice.lastRefresh_1)
                elif(index.column() == 4):
                    return QVariant(infoPrice.smartQuantite[0])
                elif(index.column() == 5):
                    return QVariant(priceToStr(infoPrice.price_10))#, infoPrice.lastRefresh_10)
                elif(index.column() == 6):
                    return QVariant(infoPrice.smartQuantite[1])
                elif(index.column() == 7):
                    return QVariant(priceToStr(infoPrice.price_100))#, infoPrice.lastRefresh_100)
                elif(index.column() == 8):
                    return QVariant(infoPrice.smartQuantite[2])
                elif(index.column() == 9):
                    return QVariant(infoPrice.smartPrice)
            else:
                if(index.column() == 9):
                    total = 0
                    for infoPrice in self.infoPrices:
                        if(infoPrice.smartPrice is not None):
                            total += infoPrice.smartPrice
                        else:
                            return "?"
                    return total
                else:
                    return QVariant()
