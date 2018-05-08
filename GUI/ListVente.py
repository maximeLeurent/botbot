from PyQt5.QtWidgets import QListView
from PyQt5 import QtCore


class ListVenteModel(QtCore.QAbstractListModel):
    def __init__(self, parent, mainWin, en_cours):
        super(QtCore.QAbstractListModel, self).__init__(parent)
        self.mainWin = mainWin
        self.selectedIng = None
        self.en_cours = en_cours
        self.listVentes = []

    def refresh(self):
        self.layoutAboutToBeChanged.emit()
        self.listVentes = self.mainWin.dbProcessor.getListVente(self.selectedIng, self.en_cours)
        self.layoutChanged.emit()

    def rowCount(self, parent):
        return len(self.listVentes)

    def majIngSelected(self, newIng):
        self.selectedIng = newIng
        self.refresh()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return str(self.listVentes[index.row()])
        elif role == QtCore.Qt.ToolTipRole:
            return "<br \>".join(str(bonus) for bonus in self.listVentes[index.row()].objet.caracs)

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

class ListVente(QListView):
    def __init__(self, parent, mainWin, en_cours):
        super(QListView,self).__init__(parent)

        self.mainWin = mainWin
        self.setModel(ListVenteModel(self, mainWin, en_cours))

    def majIngSelected(self, newIng):
        self.selectedIng = newIng
        self.model().majIngSelected(newIng)
