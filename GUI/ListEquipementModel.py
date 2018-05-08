from PyQt5 import QtCore
#from MainWindow import mainwin

class ListEquipementModel(QtCore.QAbstractListModel):
    def __init__(self, parent, mainWin):
        QtCore.QAbstractListModel.__init__(self, parent)
        #self.findMainWindow()
        self.mainWin = mainWin
        self.refresh()

    # def findMainWindow(self):
    #     objet = self
    #     for i in range(1000):
    #         objet = objet.parent()
    #         if(type(objet)== "MainWindow"):
    #             self.mainWin = objet
    #             return
    #         elif not objet:
    #             raise Exception("Unable to find the mainWindow by getting the parent")
    #     raise Exception("Unable to find the mainWindow by getting the parent")


    def refresh(self):
        self.layoutAboutToBeChanged.emit()
        self.items = self.mainWin.dbProcessor.getListItemCraftable()
        self.layoutChanged.emit()

    def rowCount(self, parent):
        return len(self.items)+1

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            if index.row() == 0:
                return ""
            value = self.items[index.row()-1]
            return "%s" % ( value.nom)

    def getEquipement(self, index):
        if index == 0:
            return None
        return self.items[index-1]
